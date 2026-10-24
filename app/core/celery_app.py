import time
from celery import Celery

celery_app=Celery(
    "ticketstorm",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)

@celery_app.task
def generate_and_send_ticket_pdf(ticket_id: int, user_email: str):
    """
    имитация генерации пдф и отправки на почту за 15 секунд
    """
    print(f"[CELERY] генерируем PDF билета #{ticket_id} для {user_email}...")
    time.sleep(5)
    print(f"[CELERY] PDF создан и отправлен на почту {user_email}")
    return {"status": "SUCCESS", "ticket_id": ticket_id, "email": user_email}