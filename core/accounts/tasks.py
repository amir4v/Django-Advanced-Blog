from celery import shared_task
from time import sleep
from core.celery import app
import logging


# @app.task
@shared_task
def send_email_task():
    logging.error("Sending email.")
    sleep(3)
    logging.error("Email sent.")
