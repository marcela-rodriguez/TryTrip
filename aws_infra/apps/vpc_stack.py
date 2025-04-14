# import injector
# from aws_cdk import aws_ec2
#
#
# import apps
#
#
# @injector.singleton
# class DefaultVPC(aws_ec2.Vpc):
#     @injector.inject
#     def __init__(self, scope: apps.VPCStack):
#         super().__init__(
#             id="DefaultVPC",
#             scope=scope,
#             max_azs=2,
#         )

import aws_cdk as core
import injector
from aws_cdk import aws_s3

import apps

@injector.singleton
class TestBucket(aws_s3.Bucket):
    @injector.inject
    def __init__(self, scope: apps.VPCStack):
        super().__init__(
            id="TestBucket",
            scope=scope,
            removal_policy=core.RemovalPolicy.DESTROY
        )