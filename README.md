# Understand ASGI and WSGI

Didactic repository to support teaching an introduction to : wsgi, asgi, gunicorn and uvicorn

# Basics

An ASGI or WSGI application is just, from the web-server point of view, a callable with a standardised signature.
That's all.

`./wsgi/app.py` as an example for WSGI app:
```python
def app(environ, start_response):
    data = b"Hello, World! \n"
    start_response("200 OK", [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(data)))
    ])
    return iter([data])
```


`./asgi/app.py` as an example for ASGI app:

```python
async def app(scope, receive, send):
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [[b"content-type", b"text/plain"]],
        }
    )
    await send({"type": "http.response.body", "body": b"Hello, world!"})
```

# Run them

As usual, pip install the requirements.txt in a virtualenv, and activate it.
If you just read chinese, I recommend https://docs.python.org/3/tutorial/venv.html.

## from python itself 

This is useful for debugging or local development, but not so much in production.

```
cd ./wsgi
python runfromgunicorn.py
```

and

```
cd ./asgi
python runfromuvicorn.py
```


## using gunicorn as a webserver

In both cases, 4 processes are launched to take advantage of multi-core cpus. 
With the web terminology, it's called a prefork model, and the processes are called workers.
In production, it's often recommended to use  `(2 x $num_cores) + 1` workers.

```
cd ./wsgi
gunicorn -w 4 app:app
```

and

```
cd ./asgi
uvicorn app:app --reload
```

But in a production setting, you will rather call
```
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker
```

You may wonder why gunicorn is needed.
I got confused too.
Gunicorn can be used to run straight a wsgi app (as in the previous example), but also to to run other type of workers such as [asyncio workers](https://docs.gunicorn.org/en/latest/design.html#asyncio-workers). 

This is then the role of uvicorn. It's a worker that knows how to "talk ASGI". 
Uvicorn can also work as an HTTP Server, but as Gunicorn is more mature, it's recommended to use only uvicorn as a worker.

Gunicorn is a HTTP Server, hence it's possible to let it deal with the requests itself.
Yet this is **not recommended**. A proper webserver like nginx will cover responsabilities that are not in the realm of Gunicorn (among them a protection to various kind of attacks like DDOS).
More [here](https://docs.gunicorn.org/en/latest/deploy.html).


# Load test on asgi app versus wsgi app

## 1/ Open Locust

Very useful tool to load test your application.

```
locust -f locustfile.py
```

Open the web page

## 2/ Check the result of sleep


Involves a `time.sleep(1)` for a wsgi app (to simulate blocking IO call)
```
cd ./wsgi
gunicorn -w 4 slow_app:app
```

Then open the locust web page to run your experiments (like spawing 2 user / second)

Involves a `asyncio.sleep(1)` for an asgi app (to simulate **non-blocking** IO call)

```
cd ./asgi
gunicorn slow_app:app -w 4 -k uvicorn.workers.UvicornWorker
```

Then open again the locust web page to run your experiments (like spawing 2 user / second)
