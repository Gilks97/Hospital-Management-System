from django.urls import path
from pages.views import *
from accounts.views import *

urlpatterns =[
     path('admin_home/', admin_home, name="admin_home"),
    path('department/', department, name="department"),
    path('doctor/', doctor, name="doctor"),
    path('nurse/', nurse, name="nurse"),
    path('patient/', patient, name="patient"),
    path('laboratorist/', laboratorist, name="laboratorist"),
    path('pharmacist/', pharmacist, name="pharmacist"),
    path('accountant/', accountant, name="accountant"), 
    path('settings/', settings, name="settings"),
    path('profile/', profile, name="profile"),
    path('add_department/', add_department, name="add_department"),
    # path('add_department_save/', add_department_save, name="add_department_save"),
    path('add_doctor/', add_doctor, name="add_doctor"),
]