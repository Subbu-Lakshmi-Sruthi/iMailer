from django.shortcuts import redirect

def has_profile(view_func):
    def wrapper_func(request, *args, **kargs):
        if not request.user.related_profiles.all():
            print("1")
            return redirect('profile')
        else:
            print(request.user.related_profiles.all())
            return view_func(request, *args, **kargs)
    return wrapper_func