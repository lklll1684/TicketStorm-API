from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_session
from app.schemas.schemas import EventCreate, TicketBuyRequest, TicketResponse
from app.api.crud import create_event_with_tickets, buy_ticket_transaction
from app.api.crud import get_top_events

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
        db: AsyncSession = Depends(get_async_session)
):
    ticket=await buy_ticket_transaction(db, data.event_id, data.email)
    return ticket

@router.get("/events/top")
async def top_events(db: AsyncSession = Depends(get_async_session)):
    return await get_top_events(db)