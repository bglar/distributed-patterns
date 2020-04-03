import os
import boto3
from botocore.exceptions import ClientError


def handler(event, context):
    """Cancel car booking lambda handler.

    event example::

      {tripId: some_guid}

    """
    db_client = boto3.client('dynamodb')
    bookings_tbl = os.getenv('CAR_BOOKINGS_TABLE_NAME')
    
    resp = db_client.get_item(
        TableName=bookings_tbl,
        Key={"tripId": event["tripId"]},
    )

    item = resp.get("Item") or {}
    item.update({
        "tripId": event["tripId"],
        "status": "CANCELLED",
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
                "cancelCarSuccess": False,
                "error": exc,
            }
        }
        # callback(null, response)
    
    return {
        "statusCode": 201,
        "body": {
            "cancelCarSuccess": True,
        }
    }
    # callback(null, response)
