from django.shortcuts import redirect

def has_profile(view_func):
    def wrapper_func(request, *args, **kargs):
        if not request.user.related_profiles:
            return redirect('profile')
        else:
            return view_func(request, *args, **kargs)
    return wrapper_func