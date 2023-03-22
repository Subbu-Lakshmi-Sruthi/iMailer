from django.db import models
from ckeditor.fields import RichTextField


class Mail(models.Model):
    mail_from=models.EmailField()
    reply_to=models.EmailField()
    subject=models.TextField()
    content=models.TextField()
    is_template=models.BooleanField()
    created_by = models.ForeignKey("users.Profile",on_delete=models.SET_NULL,null=True)

    def __str__(self) -> str:
        return str(self.mail_from)

class Log(models.Model):
    STATUS_CHOICES=((0,'Initialized'),(1,'Sent'),(2,'Read'))
    mail=models.ForeignKey(Mail,related_name="related_logs",on_delete=models.SET_NULL,null=True)
    mail_to=models.EmailField()
    status=models.IntegerField(choices=STATUS_CHOICES,default=0)

    def __str__(self):
        return f"{self.mail.mail_from}--{self.mail.mail_to}"
    
class Templates(models.Model):
    body = RichTextField(blank=True , null=True)