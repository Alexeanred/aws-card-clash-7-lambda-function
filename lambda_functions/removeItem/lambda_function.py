import json
import boto3
from botocore.exceptions import ClientError
import markdown
# Khởi tạo DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('ShoppingItem')

def remove_item_handler(event, context):
    # Nhận dữ liệu từ sự kiện (event)
    body = json.loads(event['body'])
    item_id = body.get('itemId')
    
    if not item_id:
        return {
            'statusCode': 400,
            'body': json.dumps('itemId is compulsory')
        }
    
    try:
        # Xóa item từ bảng DynamoDB
        table.delete_item(
            Key={
                'itemId': item_id
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps('Item is successfully deleted!')
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error when deleting item: {e.response['Error']['Message']}")
        }
