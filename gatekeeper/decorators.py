from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def is_logged_in(s):
    def login(f):
        @wraps(f)
        def wrapper(request, *args, **kwargs):
            _id = s + '_id'
            if _id in request.session:
                return f(request, *args, **kwargs)
            else:
                r = s + '-login'
                messages.add_message(request, messages.WARNING, 'Please login to access this page')
                return redirect(r)

        return wrapper

    return login
