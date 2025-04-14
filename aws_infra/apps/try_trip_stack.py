# import injector
# from aws_cdk import aws_ecs
# from aws_cdk import aws_ec2
# from aws_cdk import aws_ecr
# from aws_cdk import aws_iam
# from aws_cdk import aws_elasticloadbalancingv2
#
# from aws_cdk import aws_ecr_assets
#
# import apps
# from apps import vpc_stack
#
# @injector.singleton
# class TryTripSecurityGroup(aws_ec2.SecurityGroup):
#     @injector.inject
#     def __init__(self, scope: apps.TryTripStack, vpc: vpc_stack.DefaultVPC):
#         super().__init__(
#             id="TryTripSecurityGroup",
#             scope=scope,
#             allow_all_outbound=True,
#             vpc=vpc
#         )
#
#         self.add_ingress_rule(aws_ec2.Peer.any_ipv4(), aws_ec2.Port.tcp(80), "Allow HTTP traffic on port 80")
#
#
#
# @injector.singleton
# class TryTripCluster(aws_ecs.Cluster):
#     @injector.inject
#     def __init__(self, scope: apps.TryTripStack, vpc: vpc_stack.DefaultVPC):
#         super().__init__(
#             id="TryTripCluster",
#             scope=scope,
#             vpc=vpc,
#         )
#
# @injector.singleton
# class TryTripFargateTask(aws_ecs.FargateTaskDefinition):
#     @injector.inject
#     def __init__(self, scope: apps.TryTripStack):
#         super().__init__(
#             id="TryTripFargateTask",
#             scope=scope,
#             memory_limit_mib=512,
#             cpu=256,
#         )
#
#         self.add_container(
#             "TryTripContainer",
#             image=aws_ecs.ContainerImage.from_docker_image_asset(
#                 asset=aws_ecr_assets.DockerImageAsset(
#                     id="TryTripImage",
#                     scope=scope,
#                     directory="../backend",
#                 )
#             ),
#             memory_limit_mib=512,
#             cpu=256,
#             port_mappings=[aws_ecs.PortMapping(container_port=80)],
#             logging=aws_ecs.LogDriver.aws_logs(stream_prefix='TryTripLogs')
#         )
#
# @injector.singleton
# class TryTripLoadBalancer(aws_elasticloadbalancingv2.ApplicationLoadBalancer):
#     @injector.inject
#     def __init__(self, scope: apps.TryTripStack, vpc: vpc_stack.DefaultVPC, security_group: TryTripSecurityGroup):
#         super().__init__(
#             id="TryTripApplicationLoadBalancer",
#             scope=scope,
#             vpc=vpc,
#             internet_facing=True,
#             security_group=security_group
#         )
#
#
# @injector.singleton
# class TryTripECSFargateService(aws_ecs.FargateService):
#     @injector.inject
#     def __init__(
#             self,
#             scope:apps.TryTripStack,
#             cluster: TryTripCluster,
#             fargate_task: TryTripFargateTask,
#             security_group: TryTripSecurityGroup,
#             load_balancer: TryTripLoadBalancer
#     ):
#         super().__init__(
#             id="TryTripFargateService",
#             scope=scope,
#             cluster=cluster,
#             task_definition=fargate_task,
#             desired_count=1,
#             assign_public_ip=True,
#             security_groups=[security_group]
#         )
#
#         listener = load_balancer.add_listener('TryTripListener', port=80)
#
#         target_group = listener.add_targets('ECSFargateTargets',
#                                             port=80,
#                                             targets=[])
#
#         target_group.add_target(self)


import aws_cdk as core
import injector
from aws_cdk import aws_s3

import apps

@injector.singleton
class TestBucket(aws_s3.Bucket):
    @injector.inject
    def __init__(self, scope: apps.TryTripStack):
        super().__init__(
            id="TestBucket",
            scope=scope,
            removal_policy=core.RemovalPolicy.DESTROY
        )