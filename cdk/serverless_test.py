from attr import Attribute
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_sqs as sqs
from aws_cdk import core


class ServerlessTest(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        prefix = "vickk73stackv2"

        # # creating s3 bucket
        # bucket = s3.Bucket(
        #     self, f"{prefix}s3", removal_policy=core.RemovalPolicy.DESTROY
        # )

        # # creating sqs
        # queue = sqs.Queue(
        #     self,
        #     f"{prefix}sqs",
        #     visibility_timeout=core.Duration.seconds(300),
        #     removal_policy=core.RemovalPolicy.DESTROY,
        # )

        # creating dynamodb
        table = dynamodb.Table(
            self,
            f"{prefix}dynamodb",
            partition_key=Attribute(name="id", type=dynamodb.AttributeType.STRING),
            removal_policy=core.RemovalPolicy.DESTROY,
        )

        # # creating vpc
        # vpc = ec2.Vpc(
        #     self,
        #     f"{prefix}vpc",
        #     cidr="10.61.64.0/24",
        # )
