from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from .forms import *
from accounts.models import CustomUser, Doctor
from django.core.files.storage import FileSystemStorage
from accounts.models import *
from .forms import *
from django.db import IntegrityError
from django.db.models import Q
from .forgot import send_forgot_password_mail
from .decorators import authenticate_user


@authenticate_user(user_type='2')
def doctor_home(request):
    total_appointments = Appointment.objects.filter(doctor=request.user.doctor).count()

    context = {
        'total_appointments': total_appointments,
    }

    return render(request, "doctor_template/doctor_home_template.html", context)

def doctor_settings(request):
    return render(request, "doctor_template/doctor_profile.html")

def doctor_profile(request):
    return render(request, "doctor_template/doctor_profile.html")

@authenticate_user(user_type='2')
def doctor_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    doctor = Doctor.objects.get(admin=user)
    return render(request, "doctor_template/doctor_profile.html", {"user":user, "doctor":doctor})

def edit_doctor_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    doctor = Doctor.objects.get(admin=user)

    return render(request, "doctor_template/edit_doctor_profile.html", {"user": user, "doctor": doctor})

def submit_doctor_profile(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('doctor_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        special = request.POST.get('special')
        profile_pic = request.FILES.get('profile_pic')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            
            doctor = Doctor.objects.get(admin=customuser.id)
            doctor.mobile = mobile
            doctor.address = address
            doctor.special = special
            
            # Check if a new profile picture was uploaded
            if profile_pic:
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                doctor.profile_pic = filename
            
            doctor.save()
            
            messages.success(request, "Profile Updated Successfully")
            return redirect('edit_doctor_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('edit_doctor_profile')


@authenticate_user(user_type='2')        
def create_prescription(request):
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dispense_list') 
    else:
        form = PrescriptionForm()

    return render(request, 'doctor_template/create_prescription.html', {'form': form})

def delete_prescription(request,id):
    prod=Prescription.objects.get(id=id)
    prod.delete()
    return redirect('prescription_list')

def managePrescription(request):
    precrip=Prescription.objects.all()
    patient = Patient.objects.all()   
    context={
        "prescrips":precrip,
        "patient":patient
    }
    return render(request,'doctor_template/manage_prescription.html' ,context)

def editPrescription(request,pk):
    prescribe=Prescription.objects.get(id=pk)
    form=PrescriptionForm(instance=prescribe)
    if request.method == 'POST':
        form=PrescriptionForm(request.POST ,instance=prescribe)
        try:
            if form.is_valid():
                form.save()
                messages.success(request,'Prescription Updated successfully')
                return redirect('manage_precrip_doctor')
        except:
            messages.error(request,' Error!! Prescription Not Updated')
            return redirect('manage_precrip_doctor')
    context={
        "patient":prescribe,
        "form":form
    }

    return render(request,'doctor_template/edit_prescription.html',context)
@authenticate_user(user_type='2')
def doctor_appointments(request):
    current_doctor = request.user.doctor 

    appointments = Appointment.objects.filter(doctor=current_doctor)

    context = {
        'appointments': appointments
    }

    return render(request, "doctor_template/doctor_appointments.html", context)    
  

def add_appointment(request):
    return render(request, 'doctor_template/add_appointment.html')

def add_appointment_save(request):
    if request.method =='POST':
        patient = request.POST.get('patient')
        date = request.POST.get('date')
        time = request.POST.get('time')

        appointment = Appointment(
            patient = patient,
            date = date,
            time = time,
        )

        appointment.save()

        messages.success(request, 'Successfully added an appointment')
        return redirect('doctor_appointments')
    else:
        messages.error(request, 'Failed to add an appointment')
        return redirect('doctor_appointments')


def assinged_patient(request):
    return render(request, 'doctor_template/assigned_patients.html')
def dicharge_patient(request):
    return render(request, 'doctor_template/discharge_patient.html')

def add_appointment(request):
    return render(request, 'doctor_template/add_appointment.html')

def settings(request):
    return render(request, 'doctor_template/settings.html' )

def changepassword(request, token):
    try:
        user_obj = CustomUser.objects.get(reset_password_token=token)
    except CustomUser.DoesNotExist:
        messages.error(request, 'Invalid or expired token. Please request a new password reset.')
        return redirect('forgot_password')

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password != confirm_password:
            messages.error(request, 'The passwords do not match.')
            return redirect('change_password', token=token)

        # Set the new password using the set_password method
        user_obj.set_password(new_password)
        user_obj.reset_password_token = None  # Remove the token after the password reset
        user_obj.save()

        messages.success(request, 'Your password has been changed successfully. Please log in with your new password.')
        return redirect('login_user')

    return render(request, 'change-password.html')

def forgotpassword(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            try:
                user_obj = CustomUser.objects.get( Q(email=email) |Q(username=username))
            except CustomUser.DoesNotExist:
                messages.error(request, "No user with the provided credentials exists.")
                return redirect('forgot_password')

            token = str(uuid.uuid4())
            # Save the token to the user's model for later verification
            user_obj.reset_password_token = token
            user_obj.save()

            send_forgot_password_mail(user_obj, token)
            messages.success(request, 'An email has been sent successfully with instructions to reset your password.')
    except Exception as e:
        print(e)
    return render(request, 'forgot-password.html')

