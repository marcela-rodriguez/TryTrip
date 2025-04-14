import aws_cdk as core
from injector import inject, singleton

_DEFAULT_REGION = "us-east-1"


@singleton
class SBApp(core.App):
    @inject
    def __init__(self):
        super().__init__()


@singleton
class BudgetStack(core.Stack):
    @inject
    def __init__(self, scope: SBApp):
        super().__init__(
            id="BudgetStack",
            scope=scope,
            env=core.Environment(region=_DEFAULT_REGION)
        )


@singleton
class TryTripStack(core.Stack):
    @inject
    def __init__(self, scope: SBApp):
        super().__init__(
            id="TryTripStack",
            scope=scope,
            env=core.Environment(region=_DEFAULT_REGION)
        )


@singleton
class VPCStack(core.Stack):
    @inject
    def __init__(self, scope: SBApp):
        super().__init__(
            id="VPCStack",
            scope=scope,
            env=core.Environment(region=_DEFAULT_REGION)
        )
