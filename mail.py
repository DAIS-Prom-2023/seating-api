import os

from fastapi_mail import ConnectionConfig, MessageSchema, FastMail
from starlette.background import BackgroundTasks

from dotenv import load_dotenv

load_dotenv('.env')


class Envs:
    MAIL_USERNAME = os.getenv('PROM_USERNAME')
    MAIL_PASSWORD = os.getenv('PROM_PASSWORD')
    MAIL_FROM = os.getenv('PROM_FROM')
    MAIL_PORT = os.getenv('PROM_PORT')
    MAIL_SERVER = os.getenv('PROM_SERVER')
    MAIL_FROM_NAME = os.getenv('PROM_FROM_NAME')


conf = ConnectionConfig(
    MAIL_USERNAME=Envs.MAIL_USERNAME,
    MAIL_PASSWORD=Envs.MAIL_PASSWORD,
    MAIL_FROM=Envs.MAIL_FROM,
    MAIL_PORT=Envs.MAIL_PORT,
    MAIL_SERVER=Envs.MAIL_SERVER,
    MAIL_FROM_NAME=Envs.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER='./email'
)


def send_email_background(subject: str, email_to: str, body: dict, background_tasks: BackgroundTasks):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        template_body=body,
        subtype='html',
    )
    fm = FastMail(conf)
    background_tasks.add_task(
        fm.send_message, message, template_name='email.html')
