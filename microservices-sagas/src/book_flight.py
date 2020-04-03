import os
import boto3
from botocore.exceptions import ClientError


def handler(event, context):
    """Book Flight lambda handler.

    event example::
  
        { 
            tripId: some_guid,
            depart: london,
            departAt: some_date,
            arrive: dublin,
            arriveAt: some_date,
        }

    """
    db_client = boto3.client('dynamodb')
    bookings_tbl = os.getenv('FLIGHT_BOOKINGS_TABLE_NAME')

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
        "depart": event["depart"],
        "departAt": event["departAt"],
        "arrive": event["arrive"],
        "arriveAt": event["arriveAt"],
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
                "bookFlightSuccess": False,
                "error": exc,
                # "error": exc.message,
            }
        }
        # callback(null, response)
    
    return {
        "statusCode": 201,
        "body": {
            "bookFlightSuccess": True,
        }
    }
    # callback(null, response)
