from django.shortcuts import render, redirect
from django.contrib import messages

from accounts.models import CustomUser


# Create your views here.
def admin_home(request):
    return render(request, "pages/admin_template/admin_home_template.html")

def department(request):
    return render(request, "pages/admin_template/department_template.html")

def doctor(request):
    return render(request, "pages/admin_template/doctor_template.html")

def nurse(request):
    return render(request, "pages/admin_template/nurse_template.html")

def patient(request):
    return render(request, "pages/admin_template/patient_template.html")

def accountant(request):
    return render(request, "pages/admin_template/accountant_template.html")

def pharmacist(request):
    return render(request, "pages/admin_template/pharmacist_template.html")

def laboratorist(request):
    return render(request, "pages/admin_template/laboratorist_template.html")

def settings(request):
    return render(request, "pages/admin_template/settings_template.html")

def profile(request):
    return render(request, "pages/admin_template/profile_template.html")

def add_department(request):
    return render(request, "pages/admin_template/add_department_template.html")
def add_doctor(request):
    return render(request, "pages/admin_template/add_doctor_template.html")
def add_doctor_save(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        special = request.POST.get('special')

        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=2)
            user.doctor.address = address
            user.doctor.mobile = mobile
            user.doctor.special = special
            user.save()
            messages.success(request, "Doctor Added Successfully!")
            return redirect('add_doctor')
        except:
            messages.error(request, "Failed to Add Doctor!")
            return redirect('add_doctor')
        
    else:
        messages.error(request, "Invalid Method ")
        return redirect('add_doctor')
