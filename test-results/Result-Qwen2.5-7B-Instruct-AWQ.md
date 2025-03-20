```
more than 27min then FAILED
```

```python
Traceback (most recent call last):
  File "/usr/local/share/grad-app/venv/lib/python3.10/site-packages/httpx/_transports/default.py", line 101, in map_httpcore_exceptions
    yield
  File "/usr/local/share/grad-app/venv/lib/python3.10/site-packages/httpx/_transports/default.py", line 250, in handle_request
    resp = self._pool.handle_request(req)
  File "/usr/local/share/grad-app/venv/lib/python3.10/site-packages/httpcore/_sync/connection_pool.py", line 256, in handle_request
    raise exc from None
  File "/usr/local/share/grad-app/venv/lib/python3.10/site-packages/httpcore/_sync/connection_pool.py", line 236, in handle_request
    response = connection.handle_request(
  File "/usr/local/share/grad-app/venv/lib/python3.10/site-packages/httpcore/_sync/connection.py", line 103, in handle_request
    return self._connection.handle_request(request)
  File "/usr/local/share/grad-app/venv/lib/python3.10/site-packages/httpcore/_sync/http11.py", line 136, in handle_request
    raise exc
  File "/usr/local/share/grad-app/venv/lib/python3.10/site-packages/httpcore/_sync/http11.py", line 106, in handle_request
    ) = self._receive_response_headers(**kwargs)
  File "/usr/local/share/grad-app/venv/lib/python3.10/site-packages/httpcore/_sync/http11.py", line 177, in _receive_response_headers
    event = self._receive_event(timeout=timeout)
  File "/usr/local/share/grad-app/venv/lib/python3.10/site-packages/httpcore/_sync/http11.py", line 217, in _receive_event
    data = self._network_stream.read(
  File "/usr/local/share/grad-app/venv/lib/python3.10/site-packages/httpcore/_backends/sync.py", line 126, in read
    with map_exceptions(exc_map):
  File "/usr/lib/python3.10/contextlib.py", line 153, in __exit__
    self.gen.throw(typ, value, traceback)
  File "/usr/local/share/grad-app/venv/lib/python3.10/site-packages/httpcore/_exceptions.py", line 14, in map_exceptions
    raise to_exc(exc) from exc
httpcore.ReadTimeout: timed out

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/usr/local/share/grad-app/venv/lib/python3.10/site-packages/openai/_base_client.py", line 955, in _request
    response = self._client.send(
  File "/usr/local/share/grad-app/venv/lib/python3.10/site-packages/httpx/_client.py", line 914, in send
    response = self._send_handling_auth(
  File "/usr/local/share/grad-app/venv/lib/python3.10/site-packages/httpx/_client.py", line 942, in _send_handling_auth
    response = self._send_handling_redirects(
  File "/usr/local/share/grad-app/venv/lib/python3.10/site-packages/httpx/_client.py", line 979, in _send_handling_redirects
    response = self._send_single_request(request)
  File "/usr/local/share/grad-app/venv/lib/python3.10/site-packages/httpx/_client.py", line 1014, in _send_single_request
    response = transport.handle_request(request)
  File "/usr/local/share/grad-app/venv/lib/python3.10/site-packages/httpx/_transports/default.py", line 249, in handle_request
    with map_httpcore_exceptions():
  File "/usr/lib/python3.10/contextlib.py", line 153, in __exit__
    self.gen.throw(typ, value, traceback)
  File "/usr/local/share/grad-app/venv/lib/python3.10/site-packages/httpx/_transports/default.py", line 118, in map_httpcore_exceptions
    raise mapped_exc(message) from exc
httpx.ReadTimeout: timed out

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/usr/local/share/grad-app/openai-chatbot-console.py", line 39, in <module>
    chat_completion = client.chat.completions.create(
  File "/usr/local/share/grad-app/venv/lib/python3.10/site-packages/openai/_utils/_utils.py", line 279, in wrapper
    return func(*args, **kwargs)
  File "/usr/local/share/grad-app/venv/lib/python3.10/site-packages/openai/resources/chat/completions/completions.py", line 914, in create
    return self._post(
  File "/usr/local/share/grad-app/venv/lib/python3.10/site-packages/openai/_base_client.py", line 1242, in post
    return cast(ResponseT, self.request(cast_to, opts, stream=stream, stream_cls=stream_cls))
  File "/usr/local/share/grad-app/venv/lib/python3.10/site-packages/openai/_base_client.py", line 919, in request
    return self._request(
  File "/usr/local/share/grad-app/venv/lib/python3.10/site-packages/openai/_base_client.py", line 964, in _request
    return self._retry_request(
  File "/usr/local/share/grad-app/venv/lib/python3.10/site-packages/openai/_base_client.py", line 1057, in _retry_request
    return self._request(
  File "/usr/local/share/grad-app/venv/lib/python3.10/site-packages/openai/_base_client.py", line 964, in _request
    return self._retry_request(
  File "/usr/local/share/grad-app/venv/lib/python3.10/site-packages/openai/_base_client.py", line 1057, in _retry_request
    return self._request(
  File "/usr/local/share/grad-app/venv/lib/python3.10/site-packages/openai/_base_client.py", line 974, in _request
    raise APITimeoutError(request=request) from err
openai.APITimeoutError: Request timed out.
```
