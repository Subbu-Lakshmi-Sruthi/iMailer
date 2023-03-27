from django.shortcuts import redirect

def init_check(view_func):
    def wrapper_func(request, *args, **kargs):
        if not request.user.groups.all():
            return redirect('manage_access')
        if not request.user.related_profiles.all():
            return redirect('profile')
        else: 
            return view_func(request, *args, **kargs)
    return wrapper_func

def init_check_access(view_func):
    def wrapper_func(request, *args, **kargs):
        if not request.user.related_profiles.all():
            return redirect('profile')
        else: 
            return view_func(request, *args, **kargs)
    return wrapper_func

def init_check_profile(view_func):
    def wrapper_func(request, *args, **kargs):
        if not request.user.groups.all():
            return redirect('manage_access')
        else: 
            return view_func(request, *args, **kargs)
    return wrapper_func