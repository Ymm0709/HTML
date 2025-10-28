import socket
from typing import Callable, Dict, List, Tuple


class myflask:
    def __init__(self, host: str = "0.0.0.0", port: int = 8082):
        self.host = host
        self.port = port
        # routes: Dict[(path, method), handler]
        self.routes: Dict[Tuple[str, str], Callable[[], str]] = {}

    def route(self, path: str, methods: List[str] = None):
        if methods is None:
            methods = ["GET"]

        def decorator(func: Callable[[], str]):
            for method in methods:
                key = (path, method.upper())
                self.routes[key] = func
            return func

        return decorator

    def _handle_request(self, request: str) -> str:
        # Parse request line
        first_line = request.split("\r\n", 1)[0]
        try:
            method, path, _ = first_line.split(" ", 2)
        except ValueError:
            return self._response("Bad Request", status="400 Bad Request")

        handler = self.routes.get((path, method.upper()))
        if handler is None:
            return self._response(f"<h1>404 Not Found</h1><p>Path={path}</p>", status="404 Not Found")

        try:
            result = handler()
            # 如果handler返回的是tuple (body, status) 或 (body, status, content_type)
            if isinstance(result, tuple):
                if len(result) == 2:
                    body, status = result
                    return self._response(body, status)
                elif len(result) == 3:
                    body, status, content_type = result
                    return self._response(body, status, content_type)
            else:
                return self._response(result, status="200 OK")
        except Exception as exc:
            return self._response(f"<h1>500 Internal Server Error</h1><pre>{exc}</pre>", status="500 Internal Server Error")

    def _response(self, body, status: str = "200 OK", content_type: str = "text/html; charset=utf-8") -> bytes:
        # 如果body是bytes类型，直接使用
        if isinstance(body, bytes):
            body_bytes = body
        else:
            # 如果是字符串，转换为bytes
            if not isinstance(body, str):
                body = str(body)
            body_bytes = body.encode("utf-8")
        
        resp = (
            f"HTTP/1.1 {status}\r\n"
            f"Content-Type: {content_type}\r\n"
            f"Content-Length: {len(body_bytes)}\r\n"
            "Connection: close\r\n\r\n"
        ).encode("utf-8") + body_bytes
        return resp

    def run(self):
        with socket.socket() as s:
            s.bind((self.host, self.port))
            s.listen(5)
            print(f"服务器启动在 {self.host}:{self.port}")
            while True:
                conn, addr = s.accept()
                with conn:
                    print("连接地址：", addr)
                    request = conn.recv(4096).decode("utf-8", errors="ignore")
                    response = self._handle_request(request)
                    # response现在是bytes类型，直接发送
                    conn.sendall(response)