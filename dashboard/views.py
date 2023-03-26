from users.decorators import init_check
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, HttpResponse , redirect
from .forms import *
from .models import *
import json

# Create your views here.
@login_required(login_url="login")
@init_check
def dashboard(request):
    curr_user = request.user
    curr_user_group= curr_user.groups.all()
    curr_user_permissions = Access.objects.get(group = curr_user_group[0].id)
    if 'Dashboard' not in curr_user_permissions.menu : 
        return HttpResponse('you are not authorized here')
    
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
    curr_user = request.user
    curr_user_group= curr_user.groups.all()
    curr_user_permissions = Access.objects.get(group = curr_user_group[0].id)
    if 'Manage Templates' not in curr_user_permissions.menu : 
        return HttpResponse('you are not authorized here')
    
    if request.method == 'POST':
        body = request.POST['body']
        if body is not '' :
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
    curr_user = request.user
    curr_user_group= curr_user.groups.all()
    curr_user_permissions = Access.objects.get(group = curr_user_group[0].id)
    if 'Manage Templates' not in curr_user_permissions.menu : 
        return HttpResponse('you are not authorized here')
    
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
def update_template(request , id):
    curr_user = request.user
    curr_user_group= curr_user.groups.all()
    curr_user_permissions = Access.objects.get(group = curr_user_group[0].id)
    if 'Manage Templates' not in curr_user_permissions.menu : 
        return HttpResponse('you are not authorized here')
    
    templates = Templates.objects.get(id=id)
    form = TemplateForm(request.POST or None,instance=templates)
    if form.is_valid():
        form.save()
        return redirect('manage_templates')
    return render(request, 'dashboard/template.html', {'form': form}) 


@login_required(login_url='/login')
@init_check
def delete_template(request , id):
    curr_user = request.user
    curr_user_group= curr_user.groups.all()
    curr_user_permissions = Access.objects.get(group = curr_user_group[0].id)
    if 'Manage Templates' not in curr_user_permissions.menu : 
        return HttpResponse('you are not authorized here')
    
    template = Templates.objects.get(id=id)
    template.delete()
    return redirect('manage_templates')

@login_required(login_url='/login')
@init_check
def send_mail(request):
    curr_user = request.user
    curr_user_group= curr_user.groups.all()
    curr_user_permissions = Access.objects.get(group = curr_user_group[0].id)
    if 'Send Mail' not in curr_user_permissions.menu : 
        return HttpResponse('you are not authorized here')
    
    
    templates = Templates.objects.filter(created_by = request.user.related_profiles.first())
    public_templates = Templates.objects.filter(visibility = True).exclude(created_by = request.user.related_profiles.first())
    if request.method == "POST":
        form = MailForm(request.POST)
        if form.is_valid():
            obj = form.save()
            obj.created_by = request.user.related_profiles.first()
            obj.save()
            Log.objects.create(mail = obj, mail_to = request.POST["email_to"], status = 0)
            #Queue in Kafka Logic
    form = MailForm()
    return render(request, "dashboard/sendmail_ind.html", {"send_mail_active":True, "form":form, 'templates' : templates,
        'public_templates': public_templates,})

@login_required(login_url='/login')
@init_check
def send_mail_bulk(request):
    curr_user = request.user
    curr_user_group= curr_user.groups.all()
    curr_user_permissions = Access.objects.get(group = curr_user_group[0].id)
    if 'Send Mail' not in curr_user_permissions.menu : 
        return HttpResponse('you are not authorized here')
    
    templates = Templates.objects.filter(created_by = request.user.related_profiles.first())
    public_templates = Templates.objects.filter(visibility = True).exclude(created_by = request.user.related_profiles.first())
    if request.method == "POST":
        form = MailForm(request.POST)
        if form.is_valid():
            obj = form.save()
            obj.created_by = request.user.related_profiles.first()
            obj.save()
            recipient_list = json.loads(request.POST["recipient_list"])
            for li in range(0,recipient_list["length"]):
                Log.objects.create(mail_to = recipient_list[str(li)]["email"], mail = obj, status = 0)
                #Queue in Kafka Logic
    form = MailForm()
    return render(request, "dashboard/sendmail_bulk.html",{"send_mail_bulk_active": True, "form":form, 'templates' : templates,
        'public_templates': public_templates,})