#%%
import json
import os

import boto3
from botocore.exceptions import ClientError

CLUSTER_ARN, SECRET_ARN, DB_NAME, TABLE_NAME = (
    os.environ["CLUSTER_ARN"],
    os.environ["SECRET_ARN"],
    os.environ["DB_NAME"],
    "table",
)
sql_statement = f"""
create table {TABLE_NAME}(
    id int primary key auto_increment,
    first_name varchar(20),
    middle_name varchar(20),
    last_name varchar(20),
    age int
);
"""
dynamodb_resource = boto3.resource("dynamodb")
s3_client = boto3.client("s3")
sns_client = boto3.client("sns")
rds_client = boto3.client("rds-data")


def lambda_handler(event, context):
    # getting the payload
    print(f"Payload: {(payload := event.get('queryStringParameters'))}")

    try:
        response = client_rds.execute_statement(
            resourceArn=RDS_ARN,
            secretArn=SECRET_ARN,
            database=DB_NAME,
            sql=sql_statement,
        )
        print(json.dumps(response, indent=4))

    except ClientError as e:
        if e.response["Error"]["Code"] == "DecryptionFailureException":
            raise e
        elif e.response["Error"]["Code"] == "InternalServiceErrorException":
            raise e
        elif e.response["Error"]["Code"] == "InvalidParameterException":
            raise e
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            raise e
        elif e.response["Error"]["Code"] == "ResourceNotFoundException":
            raise e

    # # calculating input
    # try:
    #     x, y = float(payload["x"]), float(payload["y"])
    #     payload["z"] = str(
    #         {"+": x + y, "-": x - y, "*": x * y, "/": x / y}[payload["op"]]
    #     )

    # except Exception as e:
    #     print(f"Exception: {e}")
    #     return {"statusCode": "400", "body": f"Exception: {e}"}

    # # writing to dynamodb table
    # table = dynamodb_resource.Table(os.environ["TABLE_NAME"])
    # response = table.put_item(
    #     Item={"id": str(datetime.datetime.now()), "data": payload}
    # )

    # # sending response to sns
    # sns_client.publish(
    #     TopicArn=os.environ["SNS_ARN"],
    #     Message=f"HTTP Response: {response['ResponseMetadata']['HTTPStatusCode']}\nAnswer: {payload['z']}",
    #     MessageAttributes={
    #         "lambdamessage": {"DataType": "String", "StringValue": "true"}
    #     },
    # )

    # # writing to s3 bucket
    # with tempfile.TemporaryDirectory() as tempdir_path:
    #     path = os.path.join(
    #         tempdir_path,
    #         (
    #             file_name := f"{'-'.join('-'.join(str(datetime.datetime.now()).split(':')).split())}.txt"
    #         ),
    #     )
    #     with open(path, "w") as file_writer:
    #         file_writer.write(json.dumps(payload, indent=4))
    #     print(glob.glob(f"{tempdir_path}/*"))
    #     s3_client.upload_file(path, os.environ["BUCKET_NAME"], file_name)

    return {"statusCode": "200", "body": json.dumps(payload)}
