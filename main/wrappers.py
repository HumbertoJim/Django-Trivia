from django.http import HttpRequest
from django.shortcuts import redirect

from functools import wraps

def authentication_required(view_func):
    def wrapper(*args, **kwargs):
        request = kwargs.get('request')
        if request is None or not isinstance(request, HttpRequest):
            request = next((arg for arg in args if isinstance(arg, HttpRequest)), None)
        if request is not None and request.user.is_authenticated:
            return view_func(*args, **kwargs)
        return redirect('/accounts/login')
    return wrapper