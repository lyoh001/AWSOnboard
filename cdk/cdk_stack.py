from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_apigatewayv2 as apigatewayv2
from aws_cdk import aws_apigatewayv2_integrations as apigatewayv2_integrations
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_rds as rds
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_sns as sns
from aws_cdk import aws_sns_subscriptions as subs
from aws_cdk import aws_sqs as sqs
from aws_cdk import core


class CdkStack(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # prefix for resource name
        prefix = "-apse2-cdkstack"

        # # creating s3 bucket
        # bucket = s3.Bucket(
        #     self, f"s3{prefix}", removal_policy=core.RemovalPolicy.DESTROY
        # )

        # # creating dynamodb
        # table = dynamodb.Table(
        #     self,
        #     f"dynamodb{prefix}",
        #     partition_key=dynamodb.Attribute(
        #         name="id", type=dynamodb.AttributeType.STRING
        #     ),
        #     removal_policy=core.RemovalPolicy.DESTROY,
        # )

        # # creating sns and sns sub
        # topic = sns.Topic(self, f"sns{prefix}", display_name=f"sns{prefix}")
        # topic.add_subscription(subs.SmsSubscription(phone_number="61410844028"))

        # # creating sqs
        # queue = sqs.Queue(
        #     self, f"sqs{prefix}", visibility_timeout=core.Duration.seconds(300)
        # )

        # # creating lambda
        # handler = lambda_.Function(
        #     self,
        #     f"lambda{prefix}",
        #     runtime=lambda_.Runtime.PYTHON_3_8,
        #     code=lambda_.Code.asset("lambda"),
        #     handler="lambda_function.lambda_handler",
        #     memory_size=1024,
        #     environment=dict(
        #         BUCKET_NAME=bucket.bucket_name,
        #         TABLE_NAME=table.table_name,
        #         SNS_ARN=topic.topic_arn,
        #     ),
        # )

        # # creating api gateway
        # api = apigateway.RestApi(
        #     self,
        #     f"api{prefix}",
        #     rest_api_name=f"api{prefix}",
        #     description=f"api{prefix}: rest api gateway.",
        #     endpoint_configuration={"types": [apigateway.EndpointType.REGIONAL]},
        # )
        # api.root.add_method(
        #     "GET",
        #     apigateway.LambdaIntegration(
        #         handler,
        #         request_templates={"application/json": '{ "statusCode": "200" }'},
        #     ),
        # )

        # # creating and defining iam role permission
        # bucket.grant_read_write(handler)
        # table.grant_read_write_data(handler)
        # topic.grant_publish(handler)

        # # cfn output
        # core.CfnOutput(self, "api_url", value=api.url)

        # creating vpc
        vpc = ec2.Vpc(self, f"vpc{prefix}")

        # creating aurora cluster
        cluster = rds.ServerlessCluster(
            self,
            f"auroracluster{prefix}",
            engine=rds.DatabaseClusterEngine.AURORA_POSTGRESQL,
            parameter_group=rds.ParameterGroup.from_parameter_group_name(
                self, "ParameterGroup", "default.aurora-postgresql10"
            ),
            default_database_name=f"db",
            vpc=vpc,
            scaling=rds.ServerlessScalingOptions(
                auto_pause=core.Duration.minutes(10),
                min_capacity=rds.AuroraCapacityUnit.ACU_8,
                max_capacity=rds.AuroraCapacityUnit.ACU_32,
            ),
        )

        # creating lambda
        handler = lambda_.Function(
            self,
            f"lambda{prefix}",
            runtime=lambda_.Runtime.PYTHON_3_8,
            code=lambda_.Code.asset("lambda"),
            handler="lambda_function.lambda_handler",
            memory_size=1024,
            environment=dict(
                CLUSTER_ARN=cluster.cluster_arn,
                SECRET_ARN=cluster.secret.secret_arn,
                DB_NAME=f"db{prefix}",
                AWS_PYTHON_CONNECTION_REUSE_ENABLED="1",
            ),
        )

        # creating and defining iam role permission
        cluster.grant_data_api_access(handler)

        # creating api gateway
        api = apigatewayv2.HttpApi(
            self,
            f"end_point{prefix}",
            default_integration=apigatewayv2_integrations.LambdaProxyIntegration(
                handler=handler
            ),
        )

        # cfn output
        core.CfnOutput(self, "api_url", value=api.url)
