provider "aws"{
    region = var.AWS_REGION
    access_key = var.AWS_ACCESS_KEY 
    secret_key = var.AWS_SECRET_KEY
}

data "aws_security_group" "c13-default-sg" {
    id = var.SECURITY_GROUP_ID
}

data "aws_subnet" "c13-public-subnet" {
  id = var.SUBNET_ID
}

data "aws_ecr_image" "pipeline-image"{
    repository_name = "pipeline"
    image_tag = "latest"
}

data "aws_iam_role" "execution-role" {
  name = "ecsTaskExecutionRole"
}

data "aws_ecs_cluster" "c13-cluster" {
    cluster_name = "ecs-cluster"
}

resource "aws_ecs_task_definition" "pipeline_task"{
    family = "pipeline"
    network_mode = "awsvpc"
    requires_compatibilities = ["FARGATE"]
    execution_role_arn = data.aws_iam_role.execution-role.arn
    cpu = 256
    memory = 512
    container_definitions = jsonencode([{   
        name = "pipeline-container"
        image = data.aws_ecr_image.pipeline-image.image_uri
        essential = true
        portMappings = [
            {
                containerPort = 80
                hostPort = 80
            }
        ]
        environment =[
            {
                name = "AWS_ACCESS_KEY"
                value = var.AWS_ACCESS_KEY
            },
            {
                name = "AWS_SECRET_ACCESS_KEY"
                value = var.AWS_SECRET_KEY
            },
            {
                name = "BUCKET"
                value = var.BUCKET
            },
            {
                name = "DB_HOST"
                value = var.DB_HOST
            },         
            {
                name = "DB_PORT"
                value = var.DB_PORT
            },            
            {
                name = "DB_NAME"
                value = var.DB_NAME
            },            
            {
                name = "DB_USER"
                value = var.DB_USER
            },            
            {
                name = "DB_PASSWORD"
                value = var.DB_PASSWORD
            },            
            {
                name = "DB_SCHEMA"
                value = var.DB_SCHEMA
            }
        ]
    logConfiguration= {
                logDriver= "awslogs"
                options= {
                    awslogs-group= "/ecs/truck-pipeline"
                    mode= "non-blocking"
                    awslogs-create-group= "true"
                    max-buffer-size= "25m"
                    awslogs-region= "eu-west-2"
                    awslogs-stream-prefix= "ecs"}}
    }])
}

data  "aws_iam_policy_document" "schedule-trust-policy" {

    statement {
        effect = "Allow"

        principals {
            type        = "Service"
            identifiers = ["scheduler.amazonaws.com"]
        }

        actions = ["sts:AssumeRole"]
    }
}

data  "aws_iam_policy_document" "schedule-permissions-policy" {

    statement {
        effect = "Allow"

        resources = [
                aws_ecs_task_definition.pipeline_task.arn
            ]

        actions = [
            "ecs:RunTask"
        ]
    }

    statement {
        effect = "Allow"

        resources = [
            "*"
        ]

        actions = [
            "iam:PassRole"
        ]

    }

    statement {
        effect = "Allow"

        resources = [
            "arn:aws:logs:*:*:*"
        ]

        actions = [
            "logs:CreateLogStream",
            "logs:PutLogEvents",
            "logs:CreateLogGroup"
        ]
    }
}

resource "aws_iam_role" "schedule-role" {
    name               = "pipeline-scheduler-role"
    assume_role_policy = data.aws_iam_policy_document.schedule-trust-policy.json
    inline_policy {
      name = "execution-policy"
      policy = data.aws_iam_policy_document.schedule-permissions-policy.json
    } 
}

resource "aws_scheduler_schedule" "hourly-schedule" {
    name = "pipeline-schedule"
    flexible_time_window {
      mode = "OFF"
    }
    schedule_expression = "cron(2 11-20/3 * * ? *)"
    target {
        arn = data.aws_ecs_cluster.c13-cluster.arn
        role_arn = aws_iam_role.schedule-role.arn
        ecs_parameters {
          task_definition_arn = aws_ecs_task_definition.pipeline_task.arn
          launch_type = "FARGATE"
          network_configuration {
                subnets          = [data.aws_subnet.c13-public-subnet.id]
                security_groups  = [data.aws_security_group.c13-default-sg.id]
                assign_public_ip = true
            }
        }
    }
}

data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "lambda_role" {
  name               = "iam_for_lambda"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}


resource "aws_lambda_function" "report-lambda" {
  function_name = "report-lambda"
  package_type  = "Image"
  image_uri = var.IMAGE_URI
  role = aws_iam_role.lambda_role.arn

  environment {
    variables = {
      DB_HOST= var.DB_HOST
      DB_PORT=var.DB_PORT
      DB_NAME=var.DB_NAME
      DB_USER=var.DB_USER
      DB_PASSWORD=var.DB_PASSWORD
    }
  }
}