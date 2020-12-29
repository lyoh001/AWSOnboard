from aws_cdk import (
    aws_apigateway as apigateway,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_lambda as lambda_,
    aws_s3 as s3,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_sqs as sqs,
    core
)
class CdkStack(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        prefix = "vickk73"
        bucket = s3.Bucket(self, f"{prefix}s3")
        handler = lambda_.Function(self, f"{prefix}lambda", runtime=lambda_.Runtime.PYTHON_3_8, code=lambda_.Code.asset("lambda"), handler="lambda_function.lambda_handler", environment=dict(BUCKET=bucket.bucket_name))
        bucket.grant_read_write(handler)
        api = apigateway.RestApi(self, f"{prefix}api", rest_api_name=f"{prefix}api", description=f"{prefix} rest api gateway.")
        get_widgets_integration = apigateway.LambdaIntegration(handler,
                request_templates={"application/json": '{ "statusCode": "200" }'})
        api.root.add_method("GET", get_widgets_integration)

        queue = sqs.Queue(
            self, f"{prefix}sqs",
            visibility_timeout=core.Duration.seconds(300),
        )
        topic = sns.Topic(
            self, f"{prefix}sns"
        )
        topic.add_subscription(subs.SqsSubscription(queue))

        # vpc = ec2.Vpc(self, f"{prefix}vpc", cidr="10.0.0.0/16")
        # selection = vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE)
        # for subnet in selection.subnets:
        #     pass