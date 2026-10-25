from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from app.core.celery_app import generate_and_send_ticket_pdf
from app.core.celery_app import generate_and_send_ticket_pdf
from app.models.models import Event, Ticket, TicketStatus
import json
from app.core.redis import redis_client
async def create_event_with_tickets(db: AsyncSession, title:str, total_tickets: int):
    event=Event(title=title, total_tickets=total_tickets)
    db.add(event)
    await db.commit()
    await db.refresh(event)
    tickets=[Ticket(event_id=event.id, status=TicketStatus.AVAILABLE) for _ in range(total_tickets)]
    db.add_all(tickets)
    await db.commit()
    return event
async def get_top_events(db: AsyncSession):
    cached_data=await redis_client.get("top_events")
    if cached_data:
        print("достали из кэша")
        return json.loads(cached_data)
    print("читаем из базы данных")
    stmt=(
        select(Event)
        .limit(10)
    )
    result=await db.execute(stmt)
    events=result.scalars().all()
    events_data=[{"id": e.id, "title": e.title, "total_tickets": e.total_tickets} for e in events]
    await redis_client.set("top_events", json.dumps(events_data), ex=600)
    return events_data
async def invalidate_top_events_cache():
    await redis_client.delete("top_events")
async def buy_ticket_transaction(db: AsyncSession, event_id: int, user_email: str)->Ticket:
    async with db.begin():
        stmt=(
            select(Ticket)
            .where(Ticket.event_id == event_id, Ticket.status == TicketStatus.AVAILABLE)
            .limit(1)
            .with_for_update()
        )
        result=await db.execute(stmt)
        ticket=result.scalars().first()
        if not ticket:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="билеты кончились")
        ticket.status=TicketStatus.SOLD
        ticket.user_email=user_email
        await invalidate_top_events_cache()
    generate_and_send_ticket_pdf.delay(ticket.id, ticket.user_email)
    return ticket


