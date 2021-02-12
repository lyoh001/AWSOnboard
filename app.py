from aws_cdk import core

from cdk.cdk_stack import CdkStack

app = core.App()
CdkStack(app, "cdk", env={"region": "ap-southeast-2"})
app.synth()
