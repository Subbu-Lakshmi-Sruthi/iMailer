from users.decorators import init_check
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, HttpResponse , redirect
from .forms import TemplateForm
from .models import Templates

# Create your views here.
@login_required(login_url="login")
@init_check
def dashboard(request):
    return render(request, "dashboard/dashboard.html",{"dashboard_active":True})

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
@init_check
def add_template_view(request):
    if request.method == 'POST':
        body = request.POST['body']
        if body is not '' :
            print(body)
            visible = False
            if request.POST.get("visibility") == "on":
                visible = True
            template = Templates.objects.create(body=body, created_by=request.user.related_profiles.first(), name=request.POST["name"], visibility = visible)
        return redirect('manage_templates')
    form = TemplateForm()
    return render(request, 'dashboard/template.html', {'form': form, "create_template_active":True})


@login_required(login_url='/login')
@init_check
def manage_templates(request):
    templates = Templates.objects.filter(created_by = request.user.related_profiles.first())
    public_templates = Templates.objects.filter(visibility = True).exclude(created_by = request.user.related_profiles.first())
    context = {
        'templates' : templates,
        'public_templates': public_templates,
        'manage_template_active':True
    }
    return render(request , 'dashboard/managetemp.html' , context)


@login_required(login_url='/login')
@init_check
def update_view(request , id):
    templates = Templates.objects.get(id=id)
    form = TemplateForm(request.POST or None,instance=templates)
    if form.is_valid():
        form.save()
        return redirect('manage_templates')
    return render(request, 'dashboard/template.html', {'form': form}) 


@login_required(login_url='/login')
@init_check
def delete_view(request , id):
    template = Templates.objects.get(id=id)
    template.delete()
    return redirect('manage_templates')
