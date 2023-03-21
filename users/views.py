from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.
@login_required(login_url="login/")
def profile(request):
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST["first_name"]
        user.last_name = request.POST["last_name"]
        user.save()
        if user.related_profiles:
            profile = user.related_profiles.first()
            profile.mobile = request.POST["mobile"]
            profile.profile_img = request.FILES["profile_pic"]
            profile.save()
        else:
            Profile.objects.create(user = user, mobile = request.POST["mobile"], profile_img = request.FILES["profile_pic"])
    return render(request, "users/profile.html", {})