import asyncio

async def app(scope, receive, send):
    print("called")
    await asyncio.sleep(1)  # could be database or file system wait
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [[b"content-type", b"text/plain"]],
        }
    )
    print("answered")
    await send({"type": "http.response.body", "body": b"Hello, world!"})

