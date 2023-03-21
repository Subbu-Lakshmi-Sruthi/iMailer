from django.shortcuts import render
from users.decorators import has_profile
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="login/")
@has_profile()
def dashboard(request):
    return render(request, "dashboard/dashboard.html",{})