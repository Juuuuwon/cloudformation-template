import logging
from datetime import datetime

from fastapi import FastAPI, Response
import boto3
import botocore

BOTO3_CONFIG = botocore.client.Config(
    connect_timeout=1, read_timeout=1, retries={"max_attempts": 0}
)
client = boto3.client("s3", config=BOTO3_CONFIG)

logger = logging.getLogger("uvicorn")
app = FastAPI()


@app.get("/")
def hello(http_res: Response):
    http_res.status_code = 200
    return "hello"


@app.get("/health")
def health(http_res: Response):
    http_res.status_code = 200
    return "OK"


@app.get("/now")
def now(http_res: Response):
    http_res.status_code = 200
    now = datetime.now()
    logger.info(str(now))
    return str(now)


@app.get("/bucket")
def bucket(http_res: Response):
    BUCKET = "hmoon-skills.net"
    KEY = "ACCESS_TEST"

    try:
        object = client.get_object(Bucket=BUCKET, Key=KEY)
        body = object["Body"].read().decode("utf-8")
    except Exception as e:
        http_res.status_code = 400
        print(e)
        return "Could not access the file. Check the permission to access s3 object."

    http_res.status_code = 200
    return body
