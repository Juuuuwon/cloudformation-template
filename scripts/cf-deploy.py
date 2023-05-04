from typing import TypedDict, Iterable, Reversible
from threading import Thread
from sys import exit
from time import sleep
from colorama import Fore, Style

import logging
import sys

try:
    import boto3
except ImportError:
    print(f"boto3 is not installed for your interpreter.")
    exit(1)


logger = logging.getLogger()
logging.basicConfig(stream=sys.stdout)
logger.setLevel(logging.INFO)

REGION = "ap-northeast-2"
client = boto3.client("cloudformation", region_name=REGION)


def get_template_body(path: str) -> str:
    with open(path, "r") as f:
        body = f.read()
    return body


def create_stack(stack_param: dict) -> TypedDict:
    response = client.create_stack(**stack_param)
    return response


def update_stack(stack_param: dict) -> TypedDict:
    response = client.update_stack(**stack_param)
    return response


def delete_stack(stack_name) -> None:
    client.delete_stack(StackName=stack_name)
    return None


def get_capabilities(template_body):
    response = client.validate_template(TemplateBody=template_body)

    return response.get("Capabilities", [])


def wait_stack(operation, stack_name, delay=5, max_attempts=120):
    waiter = client.get_waiter(operation)

    waiter.wait(
        StackName=stack_name, WaiterConfig={"Delay": delay, "MaxAttempts": max_attempts}
    )

    return True


def build_template_params(stack_name, template_path, parameters: dict):
    template_body = get_template_body(template_path)
    param = {
        "StackName": stack_name,
        "TemplateBody": template_body,
        "Parameters": [
            {"ParameterKey": key, "ParameterValue": value}
            for key, value in parameters.items()
        ],
    }

    param["Capabilities"] = get_capabilities(template_body)

    return param


def deploy_in_order(stack_params: Iterable[dict], method=create_stack):
    if method == create_stack:
        wait_operation = "stack_create_complete"
        message = "created"
    elif method == update_stack:
        wait_operation = "stack_update_complete"
        message = "updated"
    else:
        raise ValueError(method)

    try:
        for param in stack_params:
            response = method(param)
            param["StackId"] = response["StackId"]
            logger.info(f"{param['StackName']} is being {message}")

            wait_stack(wait_operation, param["StackName"])
            logger.info(f"{param['StackName']} is {message}")
    except Exception as e:
        logger.error(e)

    return stack_params


def deploy_parallel(stack_sequences: Iterable[Iterable[dict]], method=create_stack):
    jobs = []
    for stacks in stack_sequences:
        job = Thread(target=deploy_in_order, args=[stacks, method], daemon=True)
        job.start()

        jobs.append(job)

    while list(filter(lambda job: job.is_alive(), jobs)):
        sleep(1)

    return stack_sequences


def delete_in_reverse_order(stack_params: Reversible[dict]):
    try:
        for param in reversed(stack_params):
            delete_stack(param["StackName"])
            logger.info(f"{param['StackName']} is being deleted")

            wait_stack("stack_delete_complete", param["StackName"])
            param.pop("StackId", None)
            logger.info(f"{param['StackName']} is deleted")
    except Exception as e:
        logger.error(e)

    return stack_params


def delete_parallel(stack_sequences: Iterable[Iterable[dict]]):
    jobs = []
    for stacks in stack_sequences:
        job = Thread(target=delete_in_reverse_order, args=[stacks], daemon=True)
        job.start()
        jobs.append(job)

    while list(filter(lambda job: job.is_alive(), jobs)):
        sleep(1)

    return stack_sequences


def describe_sequence(stack_sequences: Iterable[Iterable[dict]]):
    for num, stacks in enumerate(stack_sequences, start=1):
        stack_infos = [
            {
                "StackName": stack["StackName"],
                "Capabilities": stack["Capabilities"],
                "Parameters": stack["Parameters"],
            }
            for stack in stacks
        ]
        print(f"{Fore.WHITE}===== Stack sequence {num} =====")

        for info in stack_infos:
            print(
                f"{Fore.LIGHTGREEN_EX}{info['StackName']}"
                if info["Capabilities"]
                else f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}{info['StackName']}\t{info['Capabilities']}{Style.RESET_ALL}"
            )
            parameters = [
                f"{Fore.LIGHTBLACK_EX}{param['ParameterKey']}: {Fore.WHITE}{Style.BRIGHT}{param['ParameterValue']}{Style.RESET_ALL}"
                for param in info["Parameters"]
            ]
            print("\t" + "\n\t".join(parameters))

        print(f"{Fore.RESET}{Style.RESET_ALL}")
    return

def check_user_admission():
    retry = 0
    while retry < 2:
        admission = input("Coninue with those stacks? (y / N): ").lower()
        if admission == "n":
            break
        elif admission == "y":
            return
        else:
            print("Please enter 'y' or 'n'")
            retry += 1
    print("Cancelled")
    exit(0)


if __name__ == "__main__":
    codecommit_template_path = "C:\\skills\\template\\blue-green\\codecommit.yaml"
    codebuild_template_path = "C:\\skills\\template\\blue-green\\codebuild.yaml"
    codedeploy_template_path = "C:\\skills\\template\\blue-green\\codedeploy.yaml"
    codepipeline_template_path = "C:\\skills\\template\\blue-green\\codepipeline.yaml"

    apps = ["customer", "order", "product", "stress"]
    ARTIFACT_BUCKET = "wsi-hmoon-artifacts"
    CODECOMMIT_BRANCH = "main"

    codecommit_stack_params = [
        build_template_params(
            stack_name=f"dev-{app_name}-git",
            template_path=codecommit_template_path,
            parameters={"RepositoryName": f"dev-{app_name}"},
        )
        for app_name in apps
    ]

    codebuild_stack_params = [
        build_template_params(
            stack_name=f"dev-{app_name}-build",
            template_path=codebuild_template_path,
            parameters={
                "CodeBuildProjectName": f"dev-{app_name}-build",
                "CodeCommitRepositoryName": f"dev-{app_name}",
                "CodeCommitBranchName": CODECOMMIT_BRANCH,
                "ArtifactBucketName": ARTIFACT_BUCKET,
                "ECRRepositoryName": app_name,
            },
        )
        for app_name in apps
    ]

    codedeploy_stack_params = [
        build_template_params(
            stack_name=f"dev-{app_name}-deploy",
            template_path=codedeploy_template_path,
            parameters={
                "CodeDeployApplicationName": f"dev-{app_name}-deploy",
                "ECSServiceName": app_name,
                "TargetGroup1Name": f"{app_name}-1",
                "TargetGroup2Name": f"{app_name}-2",
            },
        )
        for app_name in apps
    ]

    codepipeline_stack_params = [
        build_template_params(
            stack_name=f"{REGION}-{app_name}-pipeilne",
            template_path=codepipeline_template_path,
            parameters={
                "CodePipelineName": f"dev-{app_name}-pipeline",
                "CodeCommitRepositoryName": f"dev-{app_name}",
                "CodeCommitBranchName": CODECOMMIT_BRANCH,
                "CodeBuildProjectName": f"dev-{app_name}-build",
                "CodeDeployApplicationName": f"dev-{app_name}-deploy",
                "CodeDeployDeploymentGroupName": f"wsi-cluster-{app_name}",
                "ArtifactBucketName": ARTIFACT_BUCKET,
            },
        )
        for app_name in apps
    ]

    try:
        # Define sequences which deploy commit, build, pipeline in order.
        sequences = list(
            zip(
                codecommit_stack_params,
                codebuild_stack_params,
                codedeploy_stack_params,
                codepipeline_stack_params,
            )
        )

        # Inform a user what are going to be executed
        describe_sequence(sequences)
        check_user_admission()

        # Execute
        delete_parallel(sequences)
        # deploy_parallel(sequences, method=update_stack)
    except Exception as e:
        logger.error(e)
