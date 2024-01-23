# from django.http import HttpResponseRedirect
# from django.utils.deprecation import MiddlewareMixin
# from django.shortcuts import render, redirect
# from django.urls import reverse


# class LoginCheckMiddleWare(MiddlewareMixin):
    
#     def process_view(self, request, view_func, view_args, view_kwargs):
#         print("Middleware is executing")
#         modulename = view_func.__module__
#         # print(modulename)
#         user = request.user

#         #Check whether the user is logged in or not
#         if user.is_authenticated:
#             if user.user_type == "1":
#                 if modulename == "accounts.views" or modulename == "django.views.static":
#                     pass
#                 else:
#                     return HttpResponseRedirect(reverse("admin_home"))
            
#             elif user.user_type == "2":
#                 if modulename == "accounts.DoctorViews":
#                     pass
#                 elif modulename == "accounts.views" or modulename == "django.views.static":
#                     pass
#                 else:
#                     return HttpResponseRedirect(reverse("doctor_home"))
            

#         else:
#             if request.path == reverse("show_login") or request.path == reverse("login_user"):
#                 pass
#             else:
#                 return HttpResponseRedirect(reverse("show_login"))
