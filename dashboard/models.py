from django.db import models
from ckeditor.fields import RichTextField
from users.models import *

class Mail(models.Model):
    mail_from=models.EmailField(null=True,blank=True)
    reply_to=models.EmailField()
    subject=models.CharField(null=True, blank=True, max_length=300)
    content=RichTextField(blank=True , null=True)
    created_by = models.ForeignKey("users.Profile",on_delete=models.SET_NULL,null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.mail_from)

class Log(models.Model):
    STATUS_CHOICES=((0,'Initialized'),(1,'Sent'),(2,'Read'),(3,'Failed'))
    mail=models.ForeignKey(Mail,related_name="related_logs",on_delete=models.SET_NULL,null=True)
    mail_to=models.EmailField()
    status=models.IntegerField(choices=STATUS_CHOICES,default=0)
    sent_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.mail.mail_from}--{self.mail_to}"
    
class Templates(models.Model):
    name = models.CharField(null=True, blank=True, max_length=100)
    body = RichTextField(blank=True , null=True)
    visibility = models.BooleanField(default=False) # True - Public, False - Private 
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="related_templates", null=True, blank=True)

class Config(models.Model):
    key = models.CharField(max_length=10)
    value = models.TextField()

class Unsubscribe(models.Model):
    email = models.EmailField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)