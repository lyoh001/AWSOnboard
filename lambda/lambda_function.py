import boto3
import json
import multiprocessing
import os


def lambda_handler(event, context):
    try:
        print("---------------Starting lambda function---------------")
        print(f"Total Number of CPUs: {(payload := multiprocessing.cpu_count())}")
        print("---------------Finished lambda function---------------")

        return {
            "statusCode": "200",
            "body": f"Total Number of CPUs: {payload}"
        }
        
    except Exception as e:
        print(str(e))