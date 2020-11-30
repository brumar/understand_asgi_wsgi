import time
def app(environ, start_response):
    print("called")
    time.sleep(1)  # could be database or file system wait
    data = b"Hello, World! \n"
    start_response("200 OK", [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(data)))
    ])
    print("answer")
    return iter([data])
