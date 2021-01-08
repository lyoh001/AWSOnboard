from aws_cdk import (
    core,
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_lambda as lambda_,
    aws_s3 as s3,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_sqs as sqs
)
class CdkStack(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        prefix = "vickk73"
        table = dynamodb.Table(self, f"{prefix}dynamodb", partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING))
        bucket = s3.Bucket(self, f"{prefix}s3")
        handler = lambda_.Function(self, f"{prefix}lambda", runtime=lambda_.Runtime.PYTHON_3_8, handler="lambda_function.lambda_handler", code=lambda_.Code.asset("lambda"), environment=dict(BUCKET=bucket.bucket_name, TABLE_NAME=table.table_name))
        table.grant_read_write_data(handler)
        bucket.grant_read_write(handler)
        api = apigateway.RestApi(self, f"{prefix}api", rest_api_name=f"{prefix}api", description=f"{prefix} rest api gateway.")
        api.root.add_method("GET", apigateway.LambdaIntegration(handler, request_templates={"application/json": '{ "statusCode": "200" }'}))
        queue = sqs.Queue(self, f"{prefix}sqs", visibility_timeout=core.Duration.seconds(300))
        topic = sns.Topic(self, f"{prefix}sns")
        topic.add_subscription(subs.SqsSubscription(queue))
        topic.add_subscription(subs.LambdaSubscription(handler))
        # vpc = ec2.Vpc(self, f"{prefix}vpc", cidr="10.0.0.0/16")
        # selection = vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE)
        # for subnet in selection.subnets:
        #     pass