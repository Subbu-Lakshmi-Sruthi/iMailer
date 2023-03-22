from django import forms
from .models import Templates

class TemplateForm(forms.ModelForm):
    class Meta:
        model = Templates
        exclude = ("created_by",)