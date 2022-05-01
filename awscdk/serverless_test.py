from aws_cdk import aws_apigatewayv2 as apigatewayv2
from aws_cdk import aws_apigatewayv2_integrations as apigatewayv2_integrations
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_rds as rds
from aws_cdk import aws_s3 as s3
from aws_cdk import core


class ServerlessTest(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        prefix = "serverlesstest"

        # creating s3 bucket
        # bucket = s3.Bucket(
        #     self,
        #     f"{prefix}s3",
        #     block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
        #     encryption=s3.BucketEncryption.KMS,
        #     removal_policy=core.RemovalPolicy.DESTROY,
        # )

        # # creating lambda
        # handler = lambda_.Function(
        #     self,
        #     f"lambda{prefix}",
        #     runtime=lambda_.Runtime.PYTHON_3_8,
        #     code=lambda_.Code.asset("lambda"),
        #     handler="lambda_function.lambda_handler",
        #     memory_size=1024,
        # )

        # creating vpc
        vpc = ec2.Vpc(self, f"vpc{prefix}")

        # creating aurora cluster
        cluster = rds.ServerlessCluster(
            self,
            f"auroracluster{prefix}",
            engine=rds.DatabaseClusterEngine.AURORA_MYSQL,
            deletion_protection=False,
            enable_data_api=True,
            removal_policy=core.RemovalPolicy.DESTROY,
            vpc=vpc,
        )
