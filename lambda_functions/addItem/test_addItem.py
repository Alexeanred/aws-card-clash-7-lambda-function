import json
import boto3
from moto import mock_aws  # Thay thế mock_dynamodb2 bằng mock_aws
from lambda_function import add_item_handler

@mock_aws  # Sử dụng mock_aws thay vì mock_dynamodb2
def test_handler_success():
    # Mock DynamoDB table
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table_name = "ShoppingItem"
    dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {"AttributeName": "itemId", "KeyType": "HASH"}
        ],
        AttributeDefinitions=[
            {"AttributeName": "itemId", "AttributeType": "S"}
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5}
    )

    # Tạo sự kiện giả
    event = {
        "httpMethod": "PUT",
        "body": json.dumps({
            "itemId": "345",
            "itemName": "dog"
        })
    }

    # Gọi handler và kiểm tra kết quả
    response = add_item_handler(event, None)
    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == "Item is added successfully!"

