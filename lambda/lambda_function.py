import boto3
import datetime
import json
import os
import tempfile


s3 = boto3.resource('s3')

def lambda_handler(event, context):
    print("---------------Starting lambda function---------------")
    print(f"Payload: {(payload := event.get('queryStringParameters'))}")
    try:
        x, y = float(payload["x"]), float(payload["y"])
        answer = {" ": x+y, "-": x-y, "*": x*y, "/": x/y}[payload["op"]]
        with tempfile.TemporaryDirectory() as tempdir_path:
            path = os.path.join(tempdir_path, (file_name := f"{'.'.join(str(datetime.datetime.now()).split(':'))}.txt"))
            with open(path, "w") as file_writer:
                file_writer.write(json.dumps(answer, indent=4))
                s3.meta.client.upload_file(path, os.environ["BUCKET"], file_name)
        return {"statusCode": "200", "body": f"Payload: {answer}"}

    except Exception as e:
        print(f"Exception: {e}")
        return {"statusCode": "400", "body": f"Exception: {e}"}