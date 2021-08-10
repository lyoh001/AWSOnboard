from aws_cdk import core

from awscdk.serverless_aurora import ServerlessAurora
from awscdk.serverless_dynamo import ServerlessDynamo
from awscdk.serverless_test import ServerlessTest


class AWSCdk(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ServerlessTest Stack
        serverlesstest = core.App()
        ServerlessTest(serverlesstest, "serverlesstest", env={"region": "ap-southeast-2"})

        # ServerlessDynamo Stack
        serverlessdynamo = core.App()
        ServerlessDynamo(serverlessdynamo, "serverlessdynamo", env={"region": "ap-southeast-2"})

        # ServerlessAurora Stack
        serverlessaurora = core.App()
        ServerlessAurora(serverlessaurora, "serverlessaurora", env={"region": "ap-southeast-2"})
