def lambda_handler(event, context):
    try:
        print("---------------Starting lambda function---------------")
        print(f"Payload: {(payload := event.get('queryStringParameters'))}")
        x, y = float(payload["x"]), float(payload["y"])
        return_val = {" ": x+y, "-": x-y, "*": x*y, "/": x/y}[payload["op"]]
        return {"statusCode": "200", "body": f"Payload: {return_val}"}

    except Exception as e:
        print(f"Exception: {e}")
        return {"statusCode": "400", "body": f"Exception: {e}"}