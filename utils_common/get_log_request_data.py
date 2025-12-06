from fastapi import Request

async def log_all_request_data(request: Request) -> None:
    headers = dict(request.headers)
    body = await request.body()
    body_str = await request.body()
    body_str = body_str.decode('utf-8')
    request_json = await request.json()

    print(f"REQUEST DATA: "
          f"method: {request.method}, url: {request.url}\n"
          f"headers: {headers}\n"
          f"query params: {request.query_params or "None"}\n"
          f"raw body: {body}\n"
          f"body string: {body_str}\n"
          f"request json: {request_json}\n")
