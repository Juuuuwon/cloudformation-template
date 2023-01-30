# Example cloudwatch dashboard

```json
{
    "widgets": [
        {
            "height": 6,
            "width": 6,
            "y": 0,
            "x": 0,
            "type": "metric",
            "properties": {
                "metrics": [
                    [ "CWAgent", "mem_used_percent", "AutoScalingGroupName", "product-api-asg" ]
                ],
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "title": "product-api-memory",
                "period": 60,
                "stat": "Average"
            }
        },
        {
            "height": 6,
            "width": 6,
            "y": 0,
            "x": 6,
            "type": "metric",
            "properties": {
                "metrics": [
                    [ "AWS/EC2", "CPUUtilization", "AutoScalingGroupName", "product-api-asg" ]
                ],
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "title": "product-api-cpu",
                "period": 60,
                "stat": "Average"
            }
        },
        {
            "height": 6,
            "width": 6,
            "y": 0,
            "x": 12,
            "type": "metric",
            "properties": {
                "metrics": [
                    [ "AWS/EC2", "NetworkIn", "AutoScalingGroupName", "product-api-asg" ],
                    [ ".", "NetworkOut", ".", "." ]
                ],
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "title": "product-api-network",
                "period": 60,
                "stat": "Average"
            }
        },
        {
            "height": 6,
            "width": 6,
            "y": 0,
            "x": 18,
            "type": "metric",
            "properties": {
                "metrics": [
                    [ "AWS/EC2", "EBSReadBytes", "AutoScalingGroupName", "product-api-asg" ],
                    [ ".", "EBSWriteBytes", ".", "." ]
                ],
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "title": "product-api-disk",
                "period": 60,
                "stat": "Average"
            }
        },
        {
            "height": 6,
            "width": 6,
            "y": 6,
            "x": 0,
            "type": "metric",
            "properties": {
                "metrics": [
                    [ "AWS/ApplicationELB", "TargetResponseTime", "LoadBalancer", "app/product-ext/4f884ab84331588e" ]
                ],
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "title": "ResponseTime",
                "period": 60,
                "stat": "Average"
            }
        },
        {
            "height": 6,
            "width": 6,
            "y": 6,
            "x": 12,
            "type": "metric",
            "properties": {
                "metrics": [
                    [ "AWS/ApplicationELB", "HTTPCode_Target_5XX_Count", "LoadBalancer", "app/product-ext/4f884ab84331588e", { "label": "HTTPCode_Target_5XX_Count" } ],
                    [ ".", "HTTPCode_ELB_5XX_Count", ".", "app/product-ext/15550a6334e7292e" ]
                ],
                "period": 60,
                "region": "us-east-1",
                "stat": "Sum",
                "title": "HTTP 5XXs",
                "yAxis": {
                    "left": {
                        "min": 0
                    }
                },
                "view": "timeSeries",
                "stacked": false
            }
        },
        {
            "type": "metric",
            "x": 6,
            "y": 6,
            "width": 6,
            "height": 6,
            "properties": {
                "metrics": [
                    [ "AWS/ApplicationELB", "RequestCount", "LoadBalancer", "app/product-ext/4f884ab84331588e" ]
                ],
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "stat": "Sum",
                "period": 60
            }
        }
    ]
}
```