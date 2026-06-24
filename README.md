# serverless-student-records-api
Serverless REST API built with AWS API Gateway, Lambda, DynamoDB and IAM
Serverless Student Records API
A production-style serverless REST API built on AWS using API Gateway, Lambda, DynamoDB, and IAM — following least-privilege security principles.

AWS Services Used

ServicePurposeAPI GatewayExposes HTTP endpoints to the internetLambda (Python 3.12)Processes POST / GET / DELETE logicDynamoDBStores student records (On-Demand)IAMLeast-privilege role for LambdaCloudWatchLambda execution logs and error alarms

  Service                            Purpose 
API Gateway                Exposes HTTP endpoints to the interne
Lambda (Python 3.12)       Processes POST / GET / DELETE logic
DynamoDB                   Stores student records (On-Demand)
IAM                        Least-privilege role for Lambda
CloudWatch                 Lambda execution logs and error alarms

**API Endpoints**
POST /student
Add a new student record.
Request:
curl -X POST https://<your-api-id>.execute-api.us-east-1.amazonaws.com/prod/student \
  -H "Content-Type: application/json" \
  -d '{"student_id": "STU001", "name": "Roronoa Zoro", "age": 22, "course": "Cloud Computing"}'

Response:

{
  "message": "Student created",
  "student_id": "STU001"
}

GET /student/{id}
Fetch a student by ID.
Request:
curl https://<your-api-id>.execute-api.us-east-1.amazonaws.com/prod/student/STU001

Response:

{
  "student_id": "STU001",
  "name": "Roronoa Zoro",
  "age": 22,
  "course": "Cloud Computing"
}

DELETE /student/{id}
Delete a student record.
Request:
curl -X DELETE https://<your-api-id>.execute-api.us-east-1.amazonaws.com/prod/student/STU001

Response:

{
  "message": "Student deleted",
  "student_id": "STU001"
}

IAM Policy (Least Privilege)
Lambda is granted only the three actions it needs, scoped to the specific table ARN:

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:PutItem",
        "dynamodb:GetItem",
        "dynamodb:DeleteItem"
      ],
      "Resource": "arn:aws:dynamodb:us-east-1:<account-id>:table/StudentRecords"
    }
  ]
}

**Project Setup**
Prerequisites
* AWS account with console access
* Basic understanding of Python

**Steps to Reproduce**
1.Create DynamoDB table StudentRecords with student_id (String) as partition key
2.Create Lambda function studentRecordsHandler (Python 3.12)
3.Paste Lambda code from lambda_function.py
4.Attach IAM inline policy to Lambda role
5.Create REST API in API Gateway
6.Create resources: /student (POST) and /student/{id} (GET, DELETE)
7.Enable Lambda Proxy Integration on all methods
8.Deploy to prod stage
9.Test using curl commands above

**Monitoring**
* CloudWatch log group: /aws/lambda/studentRecordsHandler
* Logs capture every Lambda invocation including cold starts
* Error alarm configured: triggers on any Lambda error within 5 minutes
