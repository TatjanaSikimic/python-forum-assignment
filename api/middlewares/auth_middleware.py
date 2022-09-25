import time

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware


async def add_process_time_header(request: Request, call_next):
    print('aaa')
    start_time = time.time()
    print("URL:",request.base_url)
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
            some_attribute: str,
    ):
        super().__init__(app)
        self.some_attribute = some_attribute

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

