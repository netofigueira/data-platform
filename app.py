#!/usr/bin/env python3
import os

import aws_cdk as cdk
from data_platform.data_lake.stack import DataLakeStack


app = cdk.App()
data_lake = DataLakeStack(app)

app.synth()
