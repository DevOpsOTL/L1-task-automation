#!/usr/bin/env python3
import os
import aws_cdk as cdk
from ec2_stack import EC2Stack

app = cdk.App()
EC2Stack(app, "EC2Stack", env=cdk.Environment(
    account=os.environ.get('CDK_DEFAULT_ACCOUNT'),
    region=os.environ.get('CDK_DEFAULT_REGION')
))
app.synth()