from users.decorators import init_check
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, HttpResponse , redirect
from .forms import *
from .models import *
from django.contrib import messages
from .tasks import send_mail_task,update_read_status
import json
import openai
from time import sleep
from kafka import KafkaProducer
from json import dumps
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


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



from time import sleep
from kafka import KafkaProducer
from json import dumps
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
            obj.mail_from = "lonelydeveloper2003@gmail.com"
            log = Log.objects.create(mail = obj, mail_to = request.POST["email_to"], status = 0)
            obj.content += f'<img src="http://novactf.pythonanywhere.com/get_image/{log.id}/" style="display:none;">'
            obj.save()
            Log.objects.create(mail = obj, mail_to = request.POST["email_to"], status = 0)
            # send_mail_task.delay(obj.subject,obj.content,request.POST["email_to"],obj.reply_to,log.id)
            producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x:dumps(x).encode('utf-8'))
            final_json = {}
            final_json['To'] = request.POST["email_to"]
            final_json['Subject'] = obj.subject
            final_json['Body'] = obj.content
            # final_json = json.dumps(final_json)
            producer.send('go-server-1', value=final_json)
            messages.info(request,"Mail Sent")
    form = MailForm()
    obj = Log.objects.all().first()
    return render(request, "dashboard/sendmail_ind.html", {"send_mail_active":True, "form":form, 'templates' : templates,
        'public_templates': public_templates,"obj":obj})

@login_required(login_url='/login')
@init_check
def send_mail_bulk(request):
    message1 = ""
    curr_user = request.user
    curr_user_group= curr_user.groups.all()
    curr_user_permissions = Access.objects.get(group = curr_user_group[0].id)
    if 'Send Mail' not in curr_user_permissions.menu : 
        return HttpResponse('you are not authorized here')
    
    templates = Templates.objects.filter(created_by = request.user.related_profiles.first())
    public_templates = Templates.objects.filter(visibility = True).exclude(created_by = request.user.related_profiles.first())
    if request.method == "POST":
        form = MailForm(request.POST)
        # producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x:dumps(x).encode('utf-8'))
        if form.is_valid():
            obj = form.save()
            obj.created_by = request.user.related_profiles.first()
            obj.mail_from = "lonelydeveloper2003@gmail.com"
            recipient_list = json.loads(request.POST["recipient_list"])
            obj.save()
            for li in range(0,recipient_list["length"]):
                log = Log.objects.create(mail_to = recipient_list[str(li)]["email"], mail = obj, status = 0)
                final_json = {}
                final_json["To"] = recipient_list[str(li)]["email"]
                final_json["Subject"] = obj.subject
                content_string = obj.content
                for i in range(1, int(recipient_list["vars"])+1):
                    content_string = content_string.replace("{Var"+str(i)+"}", str(recipient_list[str(li)][f"Var{i}"]))
                final_json["Body"] = content_string + f'<img src="http://novactf.pythonanywhere.com/get_image/{log.id}/" style="display:none;">'
                print(final_json)
                message1 = "Mail sent successfully"
                # #Queue in Kafka Logic
                # producer.send('go-server-1', value=final_json)
                # sleep(5)
                
    form = MailForm()
    return render(request, "dashboard/compose.html",{"send_mail_bulk_active": True, "form":form, 'templates' : templates,
        'public_templates': public_templates,"message1":message1})

@login_required(login_url='/login')
@init_check
def logs(request):
    logs = Log.objects.filter(mail__created_by = request.user.related_profiles.first())
    return render(request, "dashboard/logs.html",{"logs_active":True, "logs":logs})

from .tasks import send_mail_task,update_read_status

def read_recipient(request,id):
    update_read_status.delay(id)
    return HttpResponse("ok")

@login_required(login_url='/login')
@init_check
def compose(request):
    form = MailForm()
    templates = Templates.objects.filter(created_by = request.user.related_profiles.first())
    public_templates = Templates.objects.filter(visibility = True).exclude(created_by = request.user.related_profiles.first())
    
    return render(request, "dashboard/compose.html", {"send_mail_bulk_active": True, "form":form, 'templates' : templates,
        'public_templates': public_templates,})


openai.api_key = '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'

def chatbot_response(user_input):
# Generate a response from GPT-3
    response = openai.Completion.create(
        engine='text-davinci-002',
        prompt=user_input,
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response['choices'][0]['text']
    
def ChatbotView(request):
    if request.method == "POST":
        user_input = request.POST['user_input']
        response = chatbot_response(user_input)
        return render(request , 'dashboard/curiator.html' , {'response' : response})
    
    return render(request , 'dashboard/curiator.html')

def unsubscribe_mail_list(request, email):
    Unsubscribe.objects.create(email = email)
    return HttpResponse("OK")
@csrf_exempt
def curiate_content(request):
    if request.method == "POST":
        user_input = json.loads(request.body)
        response = chatbot_response(user_input)
        return JsonResponse({'response' : response.replace("\n" ,"<br/>" ) })
    
    return render(request , 'dashboard/curiator.html')