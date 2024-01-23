from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from.models import *

# Register your models here.
class UserModel(UserAdmin):
    pass
admin.site.register(CustomUser, UserModel)

admin.site.register(AdminHims)
admin.site.register(Doctor)
admin.site.register(Nurse)
admin.site.register(Registration_clerk)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Departments)
admin.site.register(Add_diagnosis)
admin.site.register([Dealer,Dealermessage])
admin.site.register(PatientRegistration)
