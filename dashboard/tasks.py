from celery import shared_task
from django.core.mail import EmailMultiAlternatives


@shared_task()
def send_mail_task(subject,html_content,to_email,reply_to):
    from django.core.mail import EmailMultiAlternatives
    from django.utils.html import strip_tags
    from_email = "lonelydeveloper@gmail.com"
    try:
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email],reply_to=[reply_to])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
    except Exception as e:
        print(e)