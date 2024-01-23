from django.shortcuts import redirect


from django.http import HttpResponseForbidden

def authenticate_user(user_type):
    def decorator(view_func):
        def wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.user_type == user_type:
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponseForbidden("Access Denied")  # Return a 403 Forbidden response
            else:
                return redirect('login_user')  # Redirect to login page if user is not authenticated
        return wrapped_view
    return decorator

