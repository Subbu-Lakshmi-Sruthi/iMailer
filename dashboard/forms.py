from django import forms
from .models import *

class TemplateForm(forms.ModelForm):
    class Meta:
        model = Templates
        exclude = ("created_by",)

class MailForm(forms.ModelForm):
    class Meta:
        model = Mail
        exclude = ("created_by",)