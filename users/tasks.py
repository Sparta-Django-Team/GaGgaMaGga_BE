from __future__ import absolute_import, unicode_literals

from celery import shared_task

from django.core.mail.message import EmailMessage

@shared_task
def send_email(message):
    email = EmailMessage(subject=message["email_subject"], body=message["email_body"], to=[message["to_email"]])
    email.send()
