import json
import boto3
from moto import mock_aws  # Thay thế mock_dynamodb2 bằng mock_aws
from lambda_function import remove_item_handler

@mock_aws  # Sử dụng mock_aws thay vì mock_dynamodb2
def test_handler_success():
    # Mock DynamoDB table
    dynamodb = boto3.resource('dynamodb' , region_name='us-east-1')
    table_name = "ShoppingItem"
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {"AttributeName": "itemId", "KeyType": "HASH"}
        ],
        AttributeDefinitions=[
            {"AttributeName": "itemId", "AttributeType": "S"}
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5}
    )
    table.put_item(
        Item={
            'itemId': '345',
            'itemName': 'dog'
        }
    )
    # Tạo sự kiện giả
    event = {
        "httpMethod": "DELETE",
        "body": json.dumps({
            "itemId": "345"
        })
    }

    # Gọi handler và kiểm tra kết quả
    response = remove_item_handler(event, None)
    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == 'Item is successfully deleted!'