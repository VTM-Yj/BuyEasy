# addresses/decorators.py
from django.shortcuts import redirect

def session_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('/users/login/?next=' + request.path)
        return view_func(request, *args, **kwargs)
    return wrapper
