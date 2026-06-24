import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('StudentRecords')

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            if obj % 1 == 0:
                return int(obj)
            return float(obj)
        return super().default(obj)

def lambda_handler(event, context):
    method = event.get('httpMethod') or event.get('requestContext', {}).get('http', {}).get('method')
    if not method:
        return response(400, {'error': 'Could not determine HTTP method'})
    if method == 'POST':
        return create_student(event)
    elif method == 'GET':
        return get_student(event)
    elif method == 'DELETE':
        return delete_student(event)
    else:
        return response(405, {'error': 'Method Not Allowed'})

def create_student(event):
    body = json.loads(event['body'])
    table.put_item(Item=body)
    return response(201, {'message': 'Student created', 'student_id': body['student_id']})

def get_student(event):
    student_id = event['pathParameters']['id']
    result = table.get_item(Key={'student_id': student_id})
    item = result.get('Item')
    if item:
        return response(200, item)
    return response(404, {'error': 'Student not found'})

def delete_student(event):
    student_id = event['pathParameters']['id']
    table.delete_item(Key={'student_id': student_id})
    return response(200, {'message': 'Student deleted', 'student_id': student_id})

def response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(body, cls=DecimalEncoder)
    }
