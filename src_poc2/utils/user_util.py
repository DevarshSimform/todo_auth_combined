from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv

from ..configurations.settings import settings

load_dotenv()


# FastMail connection configuration
conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_USERNAME,
    MAIL_STARTTLS=settings.MAIL_TLS,
    MAIL_SSL_TLS=settings.MAIL_SSL,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER=settings.TEMPLATE_PATH
)

async def send_welcome_email(to_email: str, data: dict):
    message = MessageSchema(
        subject = "Welcome to our service!",
        recipients = [to_email],
        template_body = data,
        subtype = 'html'
    )
    mail = FastMail(conf)
    await mail.send_message(message, template_name="welcome_email.html")


def filter_dict(user_dict):
    filtered_dict = {}
    for key, value in user_dict.items():
        if value:
            filtered_dict[key] = value
    return filtered_dict