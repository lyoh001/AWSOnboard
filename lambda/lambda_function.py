def lambda_handler(event, context):
    try:
        print("---------------Starting lambda function---------------")
        print(f"Payload: {(payload := event.get('queryStringParameters'))}")
        x = float(payload["x"])
        y = float(payload["y"])
        val = {" ": x+y, "-": x-y, "*": x*y, "/": x/y}.get(payload["op"])
        return {"statusCode": "200", "body": f"Payload: {val}"}
        
    except Exception as e:
        print(f"Exception: {e}")
        return {"statusCode": "400", "body": f"Exception: {e}"}