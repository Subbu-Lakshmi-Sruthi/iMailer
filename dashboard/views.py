from django.shortcuts import render, HttpResponse , redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login


# Create your views here.
@login_required(login_url='/login')
def dashboard(request):
    return render(request, "dashboard/dashboard.html",{})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, "dashboard/signin.html",{})  