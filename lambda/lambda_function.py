import boto3
import datetime
import glob
import json
import os
import tempfile


s3 = boto3.client('s3')

def lambda_handler(event, context):
    print(f"Payload: {(payload := event.get('queryStringParameters'))}")
    try:
        x, y = float(payload["x"]), float(payload["y"])
        payload["z"] = {" ": x+y, "-": x-y, "*": x*y, "/": x/y}[payload["op"]]
        with tempfile.TemporaryDirectory() as tempdir_path:
            path = os.path.join(tempdir_path, (file_name := f"{'-'.join('-'.join(str(datetime.datetime.now()).split(':')).split())}.txt"))
            with open(path, "w") as file_writer:
                file_writer.write(json.dumps(payload, indent=4))
            print(glob.glob(f"{tempdir_path}/*"))
            s3.upload_file(path, os.environ["BUCKET"], file_name)
        return {"statusCode": "200", "body": json.dumps(payload)}

    except Exception as e:
        print(f"Exception: {e}")
        return {"statusCode": "400", "body": f"Exception: {e}"}