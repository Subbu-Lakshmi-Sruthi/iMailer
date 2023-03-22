from users.decorators import has_profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, HttpResponse , redirect
from .forms import TemplateForm
from .models import Templates

# Create your views here.
@login_required(login_url="login")
@has_profile
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

@login_required(login_url='/login')
def add_template_view(request):
    if request.method == 'POST':
        body = request.POST['body']
        if body is not '' :
            print(body)
            template = Templates.objects.create(body=body)
        return redirect('add_template_view')
    form = TemplateForm()
    return render(request, 'dashboard/template.html', {'form': form})


@login_required(login_url='/login')
def manage_templates(request):
    templates = Templates.objects.all().values()
    context = {
        'templates' : templates
    }
    return render(request , 'dashboard/managetemp.html' , context)


@login_required(login_url='/login')
def update_view(request , id):
    templates = Templates.objects.get(id=id)
    form = TemplateForm(request.POST or None,instance=templates)
    if form.is_valid():
        form.save()
        return redirect('manage_templates')
    return render(request, 'dashboard/template.html', {'form': form}) 


@login_required(login_url='/login')
def delete_view(request , id):
    template = Templates.objects.get(id=id)
    template.delete()
    return redirect('manage_templates')
