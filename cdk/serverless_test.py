from aws_cdk import aws_s3 as s3
from aws_cdk import aws_sqs as sqs
from aws_cdk import core


class ServerlessTest(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        prefix = "apse2serverlesstest"

        # creating s3 bucket
        bucket = s3.Bucket(
            self, f"s3{prefix}", removal_policy=core.RemovalPolicy.DESTROY
        )

        # creating sqs
        sqs = sqs.Queue(self, f"sqs{prefix}", removal_policy=core.RemovalPolicy.DESTROY)
