from fastapi import APIRouter

from src.infrastructure.mail import mail, create_message
# from src.celery_tasks import send_email
from src.presentation.web.schemas.email import EmailModel

email_router = APIRouter()


@email_router.post("/send_mail")
async def send_mail(emails: EmailModel):
    emails = emails.addresses

    html = "<h1>Welcome to the app</h1>"
    subject = "Welcome to our app"

    message = create_message(recipients=emails, subject=subject, body=html)
    await mail.send_message(message)

    return {"message": "Email sent successfully"}
