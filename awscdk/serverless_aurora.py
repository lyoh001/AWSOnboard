from aws_cdk import aws_apigatewayv2 as apigatewayv2
from aws_cdk import aws_apigatewayv2_integrations as apigatewayv2_integrations
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_rds as rds
from aws_cdk import core


class ServerlessAurora(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # prefix for resource name
        prefix = "serverlessaurora"

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
            # default_database_name="db",
            vpc=vpc,
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
                DB_NAME="db",
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
