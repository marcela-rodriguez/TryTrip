import injector
import aws_cdk.aws_budgets as budgets
import aws_cdk.aws_lambda as aws_lambda
import aws_cdk.aws_sns as aws_sns
import aws_cdk.aws_sns_subscriptions as subs
from aws_cdk import aws_iam

import apps

_DEFAULT_EMAIL_NOTIFICATIONS = "sanchezbuitrago@hotmail.com"

@injector.singleton
class BudgetTopic(aws_sns.Topic):
    @injector.inject
    def __init__(self, scope: apps.BudgetStack, budget_alert_lambda: "EcsStopTasksLambda"):
        super().__init__(
            scope=scope,
            id="BudgetAlertTopic"
        )

        self.add_to_resource_policy(
            statement=aws_iam.PolicyStatement(
                effect=aws_iam.Effect.ALLOW,
                principals=[aws_iam.ServicePrincipal("budgets.amazonaws.com")],
                actions= ["SNS:Publish"],
                resources=[self.topic_arn],
                sid="Allow budget to publish to SNS"
            )
        )

        self.add_subscription(subs.EmailSubscription(_DEFAULT_EMAIL_NOTIFICATIONS))
        self.add_subscription(subs.LambdaSubscription(fn=budget_alert_lambda))



@injector.singleton
class EcsStopTasksLambda(aws_lambda.Function):
    @injector.inject
    def __init__(self, scope: apps.BudgetStack):
        super().__init__(
            id="EcsStopTasksLambda",
            scope=scope,
            runtime=aws_lambda.Runtime.PYTHON_3_12,
            handler='entrypoint.handler',
            code=aws_lambda.Code.from_asset("lambdas/budget_alert")
        )

        self.add_to_role_policy(
            statement=aws_iam.PolicyStatement(
                actions=["ecs:ListTasks", "ecs:UpdateService"],
                resources=["*"]
            )
        )

@injector.singleton
class DefaultBudget(budgets.CfnBudget):
    @injector.inject
    def __init__(self, scope: apps.BudgetStack, topic: BudgetTopic) -> None:
        super().__init__(
            scope=scope,
            id="DefaultBudget",
            budget=budgets.CfnBudget.BudgetDataProperty(
                budget_type="COST",
                time_unit="MONTHLY",
                budget_limit={
                    "amount": 20,
                    "unit": "USD"
                },
                cost_types={
                    "include_tax": False,
                    "include_subscription": True,
                    "use_blended": False
                }
            ),
            notifications_with_subscribers=[
                budgets.CfnBudget.NotificationWithSubscribersProperty(
                    notification=budgets.CfnBudget.NotificationProperty(
                        comparison_operator="GREATER_THAN",
                        threshold=50,
                        threshold_type="PERCENTAGE",
                        notification_type="ACTUAL",
                    ),
                    subscribers=[
                        budgets.CfnBudget.SubscriberProperty(
                            address=_DEFAULT_EMAIL_NOTIFICATIONS,
                            subscription_type="EMAIL"
                        )
                    ]
                ),
                budgets.CfnBudget.NotificationWithSubscribersProperty(
                    notification=budgets.CfnBudget.NotificationProperty(
                        comparison_operator="GREATER_THAN",
                        threshold=75,
                        threshold_type="PERCENTAGE",
                        notification_type="ACTUAL",
                    ),
                    subscribers=[
                        budgets.CfnBudget.SubscriberProperty(
                            address=_DEFAULT_EMAIL_NOTIFICATIONS,
                            subscription_type="EMAIL"
                        )
                    ]
                ),
                budgets.CfnBudget.NotificationWithSubscribersProperty(
                    notification=budgets.CfnBudget.NotificationProperty(
                        comparison_operator="GREATER_THAN",
                        threshold=95,
                        threshold_type="PERCENTAGE",
                        notification_type="ACTUAL",
                    ),
                    subscribers=[
                        budgets.CfnBudget.SubscriberProperty(
                            address=topic.topic_arn,
                            subscription_type="SNS"
                        )
                    ]
                ),
            ]
        )
