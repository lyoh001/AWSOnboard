from aws_cdk import core

from awscdk.awscdk import AWSCdk

# AWSCdk Stack
awscdk = core.App()
AWSCdk(awscdk, "awscdk", env={"region": "ap-southeast-2"})
awscdk.synth()
