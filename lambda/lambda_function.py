def lambda_handler(event, context):
    try:
        print("---------------Starting lambda function---------------")
        print(f"Event: {event.get('queryStringParameters')}")
        print(f"Event: {type(event.get('queryStringParameters'))}")
        print("---------------Finished lambda function---------------")

        return {
            "statusCode": "200",
            "body": f"Event: {event.get('queryStringParameters')}"
        }
        
    except Exception as e:
        print(f"Exception: {e}")

        return {
            "statusCode": "400",
            "body": f"Exception: {e}"
        }