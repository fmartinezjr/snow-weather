# EventBridge Rule for scheduled Lambda invocation
resource "aws_cloudwatch_event_rule" "schedule" {
  name                = "${var.app_name}-schedule"
  description         = "Trigger snow weather check on schedule"
  schedule_expression = var.schedule_expression

  tags = var.tags
}

# EventBridge Target forLambda Function
resource "aws_cloudwatch_event_target" "lambda" {
  rule      = aws_cloudwatch_event_rule.schedule.name
  target_id = "${var.app_name}-lambda-target"
  arn       = var.lambda_arn
}

# Lambda Permission for EventBridge to invoke
resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = var.lambda_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.schedule.arn
}
