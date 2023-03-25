from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth.models import Group , User
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
@login_required(login_url="login/")
def profile(request):
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST["first_name"]
        user.last_name = request.POST["last_name"]
        user.save()
        if user.related_profiles.all():
            profile = user.related_profiles.first()
            profile.mobile = request.POST["mobile"]
            if request.FILES.get("profile_pic"):
                profile.profile_img = request.FILES["profile_pic"]
            profile.save()
        else:
            if request.FILES.get("profile_pic"):
                Profile.objects.create(user = user, mobile = request.POST["mobile"], profile_img = request.FILES["profile_pic"])
            else:
                Profile.objects.create(user = user, mobile = request.POST["mobile"])
    return render(request, "users/profile.html", {})


@login_required(login_url="login/")
def add_group(request):
    if request.method == "POST":
        groupName = request.POST['groupName']
        permissions = request.POST.getlist('permissions')
        separator = ', '
        my_string = separator.join(permissions)
        a = Group.objects.filter(name=groupName)
        if len(a) != 0 :
            messages.error(request, 'This group already exits .')
            return redirect('add_group')
        group = Group.objects.create(name = groupName)
        access = Access.objects.create(group = group , menu = my_string)
        return redirect('add_group')
    permissions = ['Dashboard' , 'Manage Templates' , 'Send Mail' , 'Manage Users' , 'Import Users' , 'Manage Groups']
    context = {
        'permissions' : permissions,    
    }
    return render(request , 'groups/add_group.html' , context)


@login_required(login_url="login/")
@csrf_exempt
def manage_access(request):
    if request.method == 'POST':
        a = json.loads(request.body)
        for i in range(0, a["length"]):
            user = User.objects.get(email = a[str(i)]["email"])
            group = Group.objects.filter(name=a[str(i)]["group"])
            user.groups.add(group[0])
            return redirect('manage_access')
          
    users = User.objects.all()
    groups = Group.objects.all()
    a = []
    for user in users:
        if not user.groups.exists():
            a.append(user)
            

    context = {
        'users' : a ,
        'groups': groups,
    }
    return render(request , 'users/manage_access.html' , context)


@login_required(login_url="login/")
def manage_permission(request):    
    accesses = Access.objects.all()
    context = {
        'accesses':accesses
    }
    return render(request , 'groups/manage_perm.html' , context)


@login_required(login_url="login/")
def manage_pre_update(request , id):
    if request.method == "POST":
        permissions = request.POST.getlist('permissions')
        print(permissions)
        separator = ', '
        my_string = separator.join(permissions)
        acc = Access.objects.get(id = id)
        acc.menu = my_string
        acc.save()
        return redirect('manage_permission')   
    
    access = Access.objects.get(id = id)
    permissions = ['Dashboard' , 'Manage Templates' , 'Send Mail' , 'Manage Users' , 'Import Users' , 'Manage Groups']
    a = access.menu
    arr = a.split(", ")
    context = {
        'name': access.group.name,
        'menu': arr,
        'permissions' : permissions,    
    }
    return render(request , 'groups/update_group.html' , context)


@login_required(login_url="login/")
def manage_pre_delete(request , id):
    acc = Access.objects.get(id = id)
    grp = Group.objects.get(name = acc.group.name)
    grp.delete()
    acc.delete()
    return redirect('manage_permission')



@login_required(login_url="login/")
@csrf_exempt
def manage_user_permission(request):
    if request.method == 'POST':
        a = json.loads(request.body)
        for i in range(0, a["length"]):
            user = User.objects.get(email = a[str(i)]["email"])
            group = Group.objects.filter(name=a[str(i)]["group"])
            current_group = user.groups.first()
            user.groups.remove(current_group)
            user.groups.add(group[0])
            return redirect('manage_access')
        
    users = User.objects.all()
    groups = Group.objects.all()
    
    a = []
    for user in users:
        if user.groups.exists():
            a.append(user)
            print(user.groups.name)
 
    context = {
        'users' : a ,
        'groups': groups,
    }
    return render(request , 'users/update_access.html' , context)
    


