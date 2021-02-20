from aws_cdk import core

from cdk.serverless_aurora import ServerlessAurora
from cdk.serverless_dynamo import ServerlessDynamo

# ServerlessDynamo Stack
serverlessdynamo = core.App()
ServerlessDynamo(serverlessdynamo, "serverlessdynamo", env={"region": "ap-southeast-2"})
serverlessdynamo.synth()

# ServerlessAurora Stack
serverlessaurora = core.App()
ServerlessAurora(serverlessaurora, "serverlessaurora", env={"region": "ap-southeast-2"})
serverlessaurora.synth()
