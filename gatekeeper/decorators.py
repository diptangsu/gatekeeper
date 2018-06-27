from django.shortcuts import redirect
from django.contrib import messages


def is_logged_in(s):
    def login(f):
        def wrapper(request):
            _id = s + '_id'
            if _id in request.session:
                return f(request)
            else:
                r = s + '-login'
                messages.add_message(request, messages.WARNING, 'Please login to visit the dashboard')
                return redirect(r)

        return wrapper

    return login
