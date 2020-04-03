import os
import boto3
from botocore.exceptions import ClientError


def handler(event, context):
    """Book Hotel lambda handler.

    event example::

      { 
          tripId: some_guid,
          hotel: holiday inn,
          checkIn: some_date,
          checkOut: some_date,
      }

    """
    db_client = boto3.client('dynamodb')
    bookings_tbl = os.getenv('HOTEL_BOOKINGS_TABLE_NAME')

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
        "hotel": event["hotel"],
        "checkIn": event["checkIn"],
        "checkOut": event["checkOut"],
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
                "bookHotelSuccess": False,
                "error": exc,
                # "error": exc.message,
            }
        }
        # callback(null, response)
    
    return {
        "statusCode": 201,
        "body": {
            "bookHotelSuccess": True,
        }
    }
    # callback(null, response)
