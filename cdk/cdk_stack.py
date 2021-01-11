from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_sns as sns
from aws_cdk import aws_sns_subscriptions as subs
from aws_cdk import aws_sqs as sqs
from aws_cdk import core


class CdkStack(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # prefix for resource names
        prefix = "vickk73"

        # creating s3 bucket
        bucket = s3.Bucket(self, f"{prefix}s3", removal_policy=core.RemovalPolicy.DESTROY)

        # creating dynamodb
        table = dynamodb.Table(self, f"{prefix}dynamodb", partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING), removal_policy=core.RemovalPolicy.DESTROY)

        # creating sqs
        queue = sqs.Queue(self, f"{prefix}sqs", visibility_timeout=core.Duration.seconds(300))

        # creating sns and sns sub
        topic = sns.Topic(self, f"{prefix}sns", display_name=f"{prefix} sns")
        topic.add_subscription(subs.SmsSubscription(phone_number="61410844028"))

        # creating lambda
        handler = lambda_.Function(self, f"{prefix}lambda", runtime=lambda_.Runtime.PYTHON_3_8, handler="lambda_function.lambda_handler", code=lambda_.Code.asset("lambda"), environment=dict(BUCKET_NAME=bucket.bucket_name, TABLE_NAME=table.table_name, SNS_ARN=topic.topic_arn))

        # creating and defining iam role permission
        bucket.grant_read_write(handler)
        table.grant_read_write_data(handler)
        topic.grant_publish(handler)

        # creating api gateway
        api = apigateway.RestApi(self, f"{prefix}api", rest_api_name=f"{prefix}api", description=f"{prefix} rest api gateway.", endpoint_configuration={"types": [apigateway.EndpointType.REGIONAL]})
        api.root.add_method("GET", apigateway.LambdaIntegration(handler, request_templates={"application/json": '{ "statusCode": "200" }'}))

        # creating vpc
        # vpc = ec2.Vpc(self, f"{prefix}vpc", cidr="10.0.0.0/16")
        # selection = vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE)
        # for subnet in selection.subnets:
        #     pass

# from aws_cdk import (
#     aws_sqs as sqs,
#     aws_iam as iam,
#     aws_apigateway as apigw,
#     aws_lambda as _lambda,
#     aws_lambda_event_sources as lambda_event_source,
#     core
# )
# class CdkStack(core.Stack):
#     def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
#         super().__init__(scope, construct_id, **kwargs)

#         #Create the SQS queue
#         queue = sqs.Queue(self, "SQSQueue")

#         #Create the API GW service role with permissions to call SQS
#         rest_api_role = iam.Role(
#             self,
#             "RestAPIRole",
#             assumed_by=iam.ServicePrincipal("apigateway.amazonaws.com"),
#             managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSQSFullAccess")]
#         )

#         #Create an API GW Rest API
#         base_api = apigw.RestApi(self, 'ApiGW',rest_api_name='TestAPI')

#         #Create a resource named "example" on the base API
#         api_resource = base_api.root.add_resource('example')


#         #Create API Integration Response object: https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_apigateway/IntegrationResponse.html
#         integration_response = apigw.IntegrationResponse(
#             status_code="200",
#             response_templates={"application/json": ""},

#         )

#         #Create API Integration Options object: https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_apigateway/IntegrationOptions.html
#         api_integration_options = apigw.IntegrationOptions(
#             credentials_role=rest_api_role,
#             integration_responses=[integration_response],
#             request_templates={"application/json": "Action=SendMessage&MessageBody=$input.body"},
#             passthrough_behavior=apigw.PassthroughBehavior.NEVER,
#             request_parameters={"integration.request.header.Content-Type": "'application/x-www-form-urlencoded'"},
#         )

#         #Create AWS Integration Object for SQS: https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_apigateway/AwsIntegration.html
#         api_resource_sqs_integration = apigw.AwsIntegration(
#             service="sqs",
#             integration_http_method="POST",
#             path="{}/{}".format(core.Aws.ACCOUNT_ID, queue.queue_name),
#             options=api_integration_options
#         )

#         #Create a Method Response Object: https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_apigateway/MethodResponse.html
#         method_response = apigw.MethodResponse(status_code="200")

#         #Add the API GW Integration to the "example" API GW Resource
#         api_resource.add_method(
#             "POST",
#             api_resource_sqs_integration,
#             method_responses=[method_response]
#         )

#         #Creating Lambda function that will be triggered by the SQS Queue
#         sqs_lambda = _lambda.Function(self,'SQSTriggerLambda',
#             handler='lambda_function.lambda_handler',
#             runtime=_lambda.Runtime.PYTHON_3_8,
#             code=_lambda.Code.asset('lambda'),
#         )

#         #Create an SQS event source for Lambda
#         sqs_event_source = lambda_event_source.SqsEventSource(queue)

#         #Add SQS event source to the Lambda function
#         sqs_lambda.add_event_source(sqs_event_source)