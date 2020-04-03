import os
import boto3
from botocore.exceptions import ClientError


def handler(event, context):
    """Book Car lambda handler.

    event example::

        { 
            tripId: some_guid,
            car: volvo,
            carFrom: some_date,
            carTo: some_date
        }

    """
    db_client = boto3.client('dynamodb')
    bookings_tbl = os.getenv('CAR_BOOKINGS_TABLE_NAME')

    if event["failBookCar"]:
        # callback("Book Car Error")
        pass

    resp = db_client.get_item(
        TableName=bookings_tbl,
        Key={"tripId": event["tripId"]},
    )

    item = resp.get("Item")
    item.update({
        "tripId": event["tripId"],
        "car": event["car"],
        "carFrom": event["carFrom"],
        "carTo": event["carTo"]
    })

    try:
        db_client.put_item(
            TableName=bookings_tbl,
            Item=item,
        )
    except ClientError as exc:
        return {
            "statusCode": 500,
            "body": {
                "bookCarSuccess": False,
                "error": exc,
                # "error": exc.message,
            }
        }
        # callback(null, response)
    
    return {
        "statusCode": 201,
        "body": {
            "bookCarSuccess": True,
        }
    }
    # callback(null, response)
