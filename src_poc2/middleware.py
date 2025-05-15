import time
from fastapi import Request

def register_middlewares(app):
    @app.middleware('http')
    async def get_process_time(request, call_next):
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response