from fastapi import FastAPI
from app.api.routes import router
from app.core.rate_limiter import RateLimitMiddleware

app = FastAPI(title="TicketStorm API")
app.add_middleware(RateLimitMiddleware)
app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "TicketStorm работает!"}