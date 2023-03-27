from django.db import models
from django.contrib.auth.models import Group, User

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, related_name="related_profiles", on_delete=models.CASCADE)
    mobile = models.CharField(max_length= 15, null=True, blank=True)
    profile_img = models.ImageField(default="user.png", upload_to="profile")

    def __str__(self):
        return self.user.email
    
class Access(models.Model):
    group = models.ForeignKey(Group, related_name="related_access", on_delete=models.CASCADE)
    menu = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.group.name
    
class Notification(models.Model):
    SUCCESS = 1
    WARNING = 2
    ERROR = 3
    type_choice = (
        (SUCCESS, "Success"),
        (WARNING, "Warning"),
        (ERROR, "Error")
    )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="related_notifications")
    message = models.TextField(null=True, blank=True)
    type = models.IntegerField(choices=type_choice, null=True, blank=True)
    priority = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.profile.user.first_name} - {self.message}"