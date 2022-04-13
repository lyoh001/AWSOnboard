import datetime
import glob
import json
import os
import tempfile

import boto3

dynamodb_resource = boto3.resource("dynamodb")
s3_client = boto3.client("s3")
sns_client = boto3.client("sns")


def lambda_handler(event, context):
    # getting the payload
    print(f"Payload: {(payload := event.get('queryStringParameters'))}")

    # calculating input
    try:
        x, y = float(payload["x"]), float(payload["y"])
        payload["z"] = str(
            {"+": x + y, "-": x - y, "*": x * y, "/": x / y}[payload["op"]]
        )

    except Exception as e:
        print(f"Exception: {e}")
        return {"statusCode": "400", "body": f"Exception: {e}"}

    # writing to dynamodb table
    table = dynamodb_resource.Table(os.environ["TABLE_NAME"])
    response = table.put_item(
        Item={"id": str(datetime.datetime.now()), "data": payload}
    )

    # sending response to sns
    sns_client.publish(
        TopicArn=os.environ["SNS_ARN"],
        Message=f"HTTP Response: {response['ResponseMetadata']['HTTPStatusCode']}\nAnswer: {payload['z']}",
        MessageAttributes={
            "lambdamessage": {"DataType": "String", "StringValue": "true"}
        },
    )

    # writing to s3 bucket
    with tempfile.TemporaryDirectory() as tempdir_path:
        path = os.path.join(
            tempdir_path,
            (
                file_name := f"{'-'.join('-'.join(str(datetime.datetime.now()).split(':')).split())}.txt"
            ),
        )
        with open(path, "w") as file_writer:
            file_writer.write(json.dumps(payload, indent=4))
        print(glob.glob(f"{tempdir_path}/*"))
        s3_client.upload_file(path, os.environ["BUCKET_NAME"], file_name)

    return {"statusCode": "200", "body": json.dumps(payload)}
