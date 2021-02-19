from aws_cdk import core

from cdk.cdk_aurora import CdkAurora
from cdk.cdk_stack import CdkStack

cdkstack = core.App()
CdkStack(cdkstack, "cdkstack", env={"region": "ap-southeast-2"})
cdkstack.synth()

cdkaurora = core.App()
CdkAurora(cdkaurora, "cdkaurora", env={"region": "ap-southeast-2"})
cdkaurora.synth()
