module "lambda" {
  source   = "./modules/lambda"
  app_name = var.app_name
  email    = var.email
  tags     = var.tags
}

module "eventbridge" {
  source              = "./modules/eventbridge"
  app_name            = var.app_name
  lambda_arn          = module.lambda.function_arn
  lambda_name         = module.lambda.function_name
  schedule_expression = var.schedule_expression
  tags                = var.tags
}
