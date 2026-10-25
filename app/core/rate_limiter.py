import time
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.redis import redis_client

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip=request.client.host if request.client else "127.0.0.1"
        current_second=int(time.time())
        redis_key=f"rate_limit:{client_ip}:{current_second}"
        request_count = await redis_client.incr(redis_key)
        if request_count==1:
            await redis_client.expire(redis_key, 2)
        if request_count>5:
            return JSONResponse(status_code=status.HTTP_429_TOO_MANY_REQUESTS, content={"detail": "Too many requests"})
        response = await call_next(request)
        return response