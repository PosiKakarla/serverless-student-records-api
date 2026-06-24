# serverless-student-records-api
Serverless REST API built with AWS API Gateway, Lambda, DynamoDB and IAM
Serverless Student Records API
A production-style serverless REST API built on AWS using API Gateway, Lambda, DynamoDB, and IAM — following least-privilege security principles.

AWS Services Used

ServicePurposeAPI GatewayExposes HTTP endpoints to the internetLambda (Python 3.12)Processes POST / GET / DELETE logicDynamoDBStores student records (On-Demand)IAMLeast-privilege role for LambdaCloudWatchLambda execution logs and error alarms


API Endpoints

POST /student

Add a new student record.

Request:

bashcurl -X POST https://<your-api-id>.execute-api.us-east-1.amazonaws.com/prod/student \
  -H "Content-Type: application/json" \
  -d '{"student_id": "STU001", "name": "Roronoa Zoro", "age": 22, "course": "Cloud Computing"}'

Response:

json{
  "message": "Student created",
  "student_id": "STU001"
}


GET /student/{id}

Fetch a student by ID.

Request:

bashcurl https://<your-api-id>.execute-api.us-east-1.amazonaws.com/prod/student/STU001

Response:

json{
  "student_id": "STU001",
  "name": "Roronoa Zoro",
  "age": 22,
  "course": "Cloud Computing"
}


DELETE /student/{id}

Delete a student record.

Request:

bashcurl -X DELETE https://<your-api-id>.execute-api.us-east-1.amazonaws.com/prod/student/STU001

Response:

json{
  "message": "Student deleted",
  "student_id": "STU001"
}


IAM Policy (Least Privilege)

Lambda is granted only the three actions it needs, scoped to the specific table ARN:

json{
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


Real Errors Encountered and Resolved

ErrorCauseFixSyntaxError: unterminated string literalSmart quotes from copy-pasteRe-pasted code from plain text editorAccessDeniedException on PutItemLambda role had no DynamoDB permissionsAttached inline IAM policyDecimal is not JSON serializableDynamoDB returns numbers as Python Decimal typeAdded custom DecimalEncoder class


Project Setup

Prerequisites


AWS account with console access
Basic understanding of Python


Steps to Reproduce


Create DynamoDB table StudentRecords with student_id (String) as partition key
Create Lambda function studentRecordsHandler (Python 3.12)
Paste Lambda code from lambda_function.py
Attach IAM inline policy to Lambda role
Create REST API in API Gateway
Create resources: /student (POST) and /student/{id} (GET, DELETE)
Enable Lambda Proxy Integration on all methods
Deploy to prod stage
Test using curl commands above



Monitoring


CloudWatch log group: /aws/lambda/studentRecordsHandler
Logs capture every Lambda invocation including cold starts
Error alarm configured: triggers on any Lambda error within 5 minutes



Key Learnings


DynamoDB is schemaless — only the partition key is mandatory per item; other attributes are flexible per record
Lambda Proxy Integration passes the full HTTP event to Lambda including httpMethod, body, and pathParameters
Cold starts add ~1000ms on first invocation; subsequent warm invocations run in ~200ms
Least privilege IAM — scope policies to specific actions and specific resource ARNs, never use wildcards in production
