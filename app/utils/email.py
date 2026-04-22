from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi.templating import Jinja2Templates
from pathlib import Path
import secrets
from datetime import datetime, timedelta
from app.core.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent.parent.parent / 'templates'
)

fastmail = FastMail(conf)
templates = Jinja2Templates(directory=Path(__file__).parent.parent.parent / 'templates')


def generate_verification_token() -> str:
    return secrets.token_urlsafe(32)


def get_token_expiry(hours: int = 24) -> datetime:
    return datetime.now() + timedelta(hours=hours)


async def send_verification_email(email: str, name: str, token: str, base_url: str = None):
    if base_url is None:
        base_url = settings.BASE_URL
    verification_link = f"{base_url}/api/v1/auth/verify?token={token}"
    
    html_content = templates.get_template("verification.html").render({
        "name": name,
        "link": verification_link
    })
    
    message = MessageSchema(
        subject="请验证您的邮箱",
        recipients=[email],
        body=html_content,
        subtype="html"
    )
    
    await fastmail.send_message(message)