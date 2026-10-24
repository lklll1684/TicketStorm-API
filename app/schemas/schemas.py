from pydantic import BaseModel, EmailStr
from app.models.models import TicketStatus

class EventCreate(BaseModel):
    title: str
    total_tickets: int

class TicketBuyRequest(BaseModel):
    event_id: int
    email: EmailStr

class TicketResponse(BaseModel):
    id: int
    event_id: int
    status: TicketStatus
    user_email: str | None
    class Config:
        from_attributes=True
