import injector
from aws_cdk import aws_ec2


import apps


@injector.singleton
class DefaultVPC(aws_ec2.Vpc):
    @injector.inject
    def __init__(self, scope: apps.VPCStack):
        super().__init__(
            id="DefaultVPC",
            scope=scope,
            max_azs=2,
        )
