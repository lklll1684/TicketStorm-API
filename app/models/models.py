import enum
from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime, Enum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class TicketStatus(str, enum.Enum):
    AVAILABLE='AVAILABLE'
    RESERVED='RESERVED'
    SOLD='SOLD'

class Event(Base):
    __tablename__ = 'events'
    id: Mapped[int]=mapped_column(primary_key=True)
    title: Mapped[str]=mapped_column(String(255), nullable=False)
    total_tickets: Mapped[int]=mapped_column(nullable=False)
    tickets: Mapped[list["Ticket"]]=relationship(back_populates="event", cascade="all, delete-orphan")

class Ticket(Base):
    __tablename__ = 'tickets'
    id: Mapped[int]=mapped_column(primary_key=True)
    event_id: Mapped[int]=mapped_column(ForeignKey('events.id'), nullable=False)
    status: Mapped[TicketStatus]=mapped_column(
        Enum(TicketStatus),
        default=TicketStatus.AVAILABLE,
        nullable=False
    )
    user_email: Mapped[str | None]=mapped_column(String(255), nullable=True)
    updated_at: Mapped[datetime]=mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    event: Mapped["Event"]=relationship(back_populates="tickets")