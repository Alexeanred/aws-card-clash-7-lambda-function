import json
import boto3
from botocore.exceptions import ClientError
import markdown
# Khởi tạo DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ShoppingItem')

def add_item_handler(event, context):
    print("Event: ",event)
    # Nhận dữ liệu từ sự kiện (event)
    body = json.loads(event['body'])
    item_id = body['itemId']
    item_name = body['itemName']
    print(body)
    print(item_id)
    
    if not item_id or not item_name:
        return {
            'statusCode': 400,
            'body': json.dumps('itemId và itemName are compulsory.')
        }
    
    try:
        # Thêm item vào bảng DynamoDB
        table.put_item(
            Item={
                'itemId': item_id,
                'itemName': item_name
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps('Item is added successfully!')
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error when add item: {e.response['Error']['Message']}")
        }
