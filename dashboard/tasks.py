from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.http import HttpResponse
from .models import Log
@shared_task()
def send_mail_task(subject,html_content,to_email,reply_to,log_id):
    from_email = "lonelydeveloper@gmail.com"
    try:
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email],reply_to=[reply_to])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
        log = Log.objects.get(id=log_id)
        log.status = 1
        log.save()
    except Exception as e:
        print(e)


@shared_task(queue='queue1')
def update_read_status(id):
    log = Log.objects.get(id=id)
    log.status = 2
    log.save()