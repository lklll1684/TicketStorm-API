from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_session
from app.core.redis import redis_client
from app.schemas.schemas import EventCreate, TicketBuyRequest, TicketResponse
from app.api.crud import create_event_with_tickets, buy_ticket_transaction
from app.api.crud import get_top_events
import json

router=APIRouter()

@router.post("/events/")
async def create_event(
        data: EventCreate,
        db: AsyncSession = Depends(get_async_session)
):
    event=await create_event_with_tickets(db, data.title, data.total_tickets)
    return {"message": "событие создано!", "event_id": event.id}

@router.post("/tickets/buy", response_model=TicketResponse)
async def buy_ticket(
        data: TicketBuyRequest,
        x_request_id: str | None= Header(None, alias="X-Request-ID"),
        db: AsyncSession = Depends(get_async_session)
):
    if x_request_id:
        cache_key=f"idempotency:{x_request_id}"
        cached_response=await redis_client.get(cache_key)
        if cached_response:
            print(f"возвращаем сохраненный ответ для ключа {x_request_id}")
            return json.loads(cached_response)
    ticket=await buy_ticket_transaction(db, data.event_id, data.email)
    response_data={
        "id": ticket.id,
        "event_id": ticket.event_id,
        "status": ticket.status,
        "user_email": ticket.user_email,
    }
    if x_request_id:
        await redis_client.set(f"idempotency:{x_request_id}", json.dumps(response_data), ex=86400)
    return response_data



@router.get("/events/top")
async def top_events(db: AsyncSession = Depends(get_async_session)):
    return await get_top_events(db)