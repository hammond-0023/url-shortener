output "function_url" {
  value = aws_lambda_function_url.api.function_url
}

output "deploy_role_arn" {
  value = aws_iam_role.deploy.arn
}
