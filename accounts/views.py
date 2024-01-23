import datetime
from datetime import date, datetime
from django import forms
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.urls import reverse
from .forms import LoginForm


from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageTemplate, Frame, Paragraph, Spacer

from accounts.models import AdminHims, Departments, CustomUser, Doctor, Nurse, Registration_clerk, PatientRegistration
from django.core.mail import send_mail

from accounts.models import *



from accounts.EmailBackEnd import EmailBackEnd
from django.contrib.auth.decorators import login_required

from .decorators import authenticate_user

# Create your views here.

def ShowLoginPage(request):
    return render (request, "login.html")

def index(request):
    return render(request, 'home.html')


def home(request):
    return render(request, "home.html")

    
def login_user(request):
    if request.method=="POST":
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            if user.user_type=="1":   
                return redirect("/admin_home")
            
            elif user.user_type == '2':
                # return HttpResponse("Doctor Login")
                return redirect('doctor_home')
                
            elif user.user_type == '3':
                # return HttpResponse("Nurse Login")
                return redirect('nurse_home')
            
            elif user.user_type == '4':
                # return HttpResponse("Reception_clerk Login")
                return redirect('registration_clerk_home')
            elif user.user_type=='7':
                return redirect('admin')          
            else:
                # return HttpResponse("Patient Login")
                return redirect('patient_home')
  
        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect("/")
        
    else:
        return render(request, "login.html")
        #return HttpResponse("<h2>Method Not Allowed<h2>")


def GetUserDetails(request):
    if request.user.is_authenticated:
        email = request.user.email    
        return HttpResponse("User : "+ request.user.email+ " Usertype : "+request.user.user_type)
    else:
        return HttpResponse("Please Login First")

        
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


###AdminViews
@authenticate_user(user_type='1')
def admin_home(request):
    return render(request, "admin_template/admin_home_template.html")

@authenticate_user(user_type='1')
def department(request):
    department = Departments.objects.all()
    context = {
        'department' : department
    }
    return render(request, "admin_template/department_template.html", context)


@authenticate_user(user_type='1')
def doctor(request):
    doctors = Doctor.objects.all()
    context = {
        'doctors':doctors
    }
    return render(request, "admin_template/doctor_template.html", context)

@authenticate_user(user_type='1')
def nurse(request):
    nurses = Nurse.objects.all()
    context = {
        'nurses' : nurses
    }
    return render(request, "admin_template/nurse_template.html", context)

@authenticate_user(user_type='1')
def patient(request):
    return render(request, "admin_template/patient_template.html")

@authenticate_user(user_type='1')
def accountant(request):
    return render(request, "admin_template/accountant_template.html")

@authenticate_user(user_type='1')
def pharmacist(request):
    pharmacist=Pharmacist.objects.all()
    context={
        'pharma':pharmacist
    }
    return render(request, "admin_template/pharmacist_template.html",context)

@authenticate_user(user_type='1')
def laboratorist(request):
    return render(request, "admin_template/laboratorist_template.html")

@authenticate_user(user_type='1')
def admin_hims_settings(request):
    return render(request, "admin_template/settings_template.html")

@authenticate_user(user_type='1')
def admin_hims_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    admin_hims = AdminHims.objects.get(admin=user)
    return render(request, "admin_template/admin_profile.html", {"user":user, "admin_hims": admin_hims})

@authenticate_user(user_type='1')
def edit_admin_hims_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    admin_hims = AdminHims.objects.get(admin=user)
    return render(request, "admin_template/edit_admin_profile.html", {"user":user, "admin_hims": admin_hims})

def submit_admin_hims_profile(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('admin_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        profile_pic = request.FILES.get('profile_pic')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
                
            admin_hims = AdminHims.objects.get(admin=customuser.id)
            # Check if a new profile picture was uploaded
            if profile_pic:
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                admin_hims.profile_pic = filename
                
            customuser.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('edit_admin_hims_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('edit_admin_hims_profile')

@authenticate_user(user_type='1')
def add_department(request):
    return render(request, "admin_template/add_department_template.html")

def add_department_save(request):
    if request.method == "POST":
        department_name = request.POST.get('department_name')
        department_description = request.POST.get('department_description')

        department = Departments(
            department_name=department_name,
            department_description=department_description
        )
        department.save()

        messages.success(request, "Department saved successfully!")
        return redirect('add_department')
    else:
        messages.error(request, "Invalid method!")
        return redirect('add_department')


# def add_department_save(request):
#     if request.method != "POST":
#         messages.error(request, "Invalid Method!")
#         return redirect('add_department')
#     else:
#         department = request.POST.get('department')
#         department = request.POST.get('department_description')
#         try:
#             department_model = Departments(department_name=department)
#             department_model.save()
#             messages.success(request, "Department Added Successfully!")
#             return redirect('add_department')
#         except:
#             messages.error(request, "Failed to Add Department!")
#             return redirect('add_department')

def manage_department(request):
    departments = Departments.objects.all()
    context = {
        "departments": departments
    }
    return render(request, 'admin_template/manage_department_template.html', context)
      
def edit_department(request, department_id):
    department = Departments.objects.get(id=department_id)
    context = {
        "department": department,
        "id": department_id
    }
    return render(request, 'admin_template/edit_department_template.html', context)


def edit_department_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method")
    else:
        department_id = request.POST.get('department_id')
        department_name = request.POST.get('department_name')
        department_description = request.POST.get('department_description')

        if department_id is not None:
            try:
                department = Departments.objects.get(id=department_id)
                department.department_name = department_name
                department.department_description = department_description
                department.save()

                messages.success(request, "Department updated successfully.")
                return redirect(reverse('edit_department', args=[department_id]))

            except Departments.DoesNotExist:
                messages.error(request, "Department does not exist.")
                return redirect(reverse('edit_department', args=[department_id]))
        else:
            messages.error(request, "Invalid department ID.")
            return redirect(reverse('edit_department', args=[department_id]))
        

def delete_department(request, department_id):
    department = Departments.objects.get(id=department_id)
    try:
        department.delete()
        messages.success(request, "Department Deleted Successfully.")
        return redirect('manage_department')
    except:
        messages.error(request, "Failed to Delete Department.")
        return redirect('manage_department')
    

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from .models import CustomUser

def add_pharmacist(request):
    return render(request, "admin_template/add_pharmacist.html")

def add_pharmacist_save(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        profile_pic = request.FILES.get('profile_pic')

        if not (first_name and last_name and username and email and password and mobile and address):
            messages.error(request, "All fields are required.")
            return redirect('pharmacist')

        try:
            # Check if the username already exists
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, "Username already exists. Please choose a different username.")
                return redirect('pharmacist')

            # Create the pharmacist user
            user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=7)
            user.pharmacist.address = address
            user.pharmacist.mobile = mobile

            if profile_pic:
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                user.pharmacist.profile_pic = filename

            user.save()
            messages.success(request, "Pharmacist added successfully!")
            return redirect('pharmacist')
        except Exception as e:
            messages.error(request, f"Failed to add pharmacist: {e}")
            return redirect('add_pharmacist')

    else:
        messages.error(request, "Invalid request method.")
        return redirect('add_pharmacist')


def manage_pharmacist(request):
    pharma = Pharmacist.objects.all()
    context = {
        "pharma": pharma
    }
    return render(request, "admin_template/manage_pharmacist.html", context)

def edit_pharmacist(request, pharma_id):
    pharma= Pharmacist.objects.get(admin=pharma_id)

    context = {
        "pharmacist": pharma,
        "id": pharma_id
    }
    return render(request, "admin_template/edit_pharmacist.html", context)


def edit_pharmacist_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        pharma_id = request.POST.get('pharmacist_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')

        # Check if a new profile picture is uploaded
        profile_pic_url = None
        if request.FILES.get('profile_pic'):
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)

        try:
            # Retrieve and update the CustomUser instance
            user = CustomUser.objects.get(id=pharma_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            # Retrieve and update the Pharmacist instance
            pharmacist = Pharmacist.objects.get(admin=pharma_id)
            pharmacist.address = address
            pharmacist.mobile = mobile
            
            # Update the profile_pic field only if profile_pic_url is not None
            if profile_pic_url:
                pharmacist.profile_pic = profile_pic_url
            pharmacist.save()

            messages.success(request, "Pharmacist Updated Successfully.")
            return redirect('/edit_pharmacist/' + pharma_id)

        except Exception as e:
            messages.error(request, f"Failed to Update pharmacist: {e}")
            return redirect('/edit_pharmacist/' + pharma_id)


def delete_pharmacist(request, pharma_id):
    try:
        user = CustomUser.objects.get(id=pharma_id)
        doctor = user.pharmacist
        user.delete()  # Delete the CustomUser objects
        doctor.delete()  # Delete the associated Doctor objects
        messages.success(request, "Doctor deleted successfully.")
        return redirect('manage_pharmacist')
    except CustomUser.DoesNotExist:
        messages.error(request, "pharmacist does not exist.")
    except Exception as e:
        messages.error(request, f"Failed to delete pharmacist: {str(e)}")
    return redirect('manage_pharmacist')

def add_doctor(request):
    return render(request, "admin_template/add_doctor_template.html")


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
        
        profile_pic = request.FILES.get('profile_pic')

        if profile_pic:
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = filename
        else:
            profile_pic_url = 'profile_pics/default_profile_pic.jpeg'
            
        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=2)
            user.doctor.address = address
            user.doctor.mobile = mobile
            user.doctor.special = special
            user.doctor.profile_pic = profile_pic_url
                
            user.save()
            messages.success(request, "Doctor Added Successfully!")
            return redirect('add_doctor')
        except:
            messages.error(request, "Failed to Add Doctor!")
            return redirect('add_doctor')
        
    else:
        messages.error(request, "Invalid Method ")
        return redirect('add_doctor')



def manage_doctor(request):
    doctors = Doctor.objects.all()
    context = {
        "doctors": doctors
    }
    return render(request, "admin_template/doctor_template.html", context)


def edit_doctor(request, doctor_id):
    doctor = Doctor.objects.get(admin=doctor_id)

    context = {
        "doctor": doctor,
        "id": doctor_id
    }
    return render(request, "admin_template/edit_doctor_template.html", context)


def edit_doctor_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        doctor_id = request.POST.get('doctor_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        special = request.POST.get('special')

        # Check if a new profile picture is uploaded
        if request.FILES.get('profile_pic'):
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None

        try:
            # UPDATE CustomUser model
            user = CustomUser.objects.get(id=doctor_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            # UPDATE Doctor model
            doctor_model = Doctor.objects.get(admin=doctor_id)
            doctor_model.address = address
            doctor_model.mobile = mobile
            doctor_model.special = special

            if profile_pic_url:
                doctor_model.profile_pic = profile_pic_url  # Update the profile_pic field

            doctor_model.save()

            messages.success(request, "Doctor Updated Successfully.")
            return redirect('/edit_doctor/'+doctor_id)

        except:
            messages.error(request, "Failed to Update doctor.")
            return redirect('/edit_doctor/'+doctor_id)

def delete_doctor(request, doctor_id):
    try:
        user = CustomUser.objects.get(id=doctor_id)
        doctor = user.doctor
        user.delete()  # Delete the CustomUser objects
        doctor.delete()  # Delete the associated Doctor objects
        messages.success(request, "Doctor deleted successfully.")
        return redirect('manage_doctor')
    except CustomUser.DoesNotExist:
        messages.error(request, "Doctor does not exist.")
    except Exception as e:
        messages.error(request, f"Failed to delete doctor: {str(e)}")
    return redirect('manage_doctor')

def laboratorist_template(request):
    return render(request, 'admin_template/laboratorist_template.html')
    
def add_nurse(request):
     return render(request, "admin_template/add_nurse_template.html")


def add_nurse_save(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        specialization = request.POST.get('specialization')
        
        profile_pic = request.FILES.get('profile_pic')

        if profile_pic:
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = filename
        else:
            profile_pic_url = 'profile_pics/default_profile_pic.jpeg'

        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=3)
            user.nurse.address = address
            user.nurse.mobile = mobile
            user.nurse.specialization = specialization
            user.nurse.profile_pic = profile_pic_url
            user.save()
            messages.success(request, "Nurse Added Successfully!")
            return redirect('add_nurse')
        except:
            messages.error(request, "Failed to Add Nurse!")
            return redirect('add_nurse')
        
    else:
        messages.error(request, "Invalid Method ")
        return redirect('add_nurse')



def manage_nurse(request):
    nurses = Nurse.objects.all()
    context = {
        "nurses": nurses
    }
    return render(request, "admin_template/nurse_template.html", context)

def edit_nurse(request, nurse_id):
    nurse = Nurse.objects.get(admin=nurse_id)

    context = {
        "nurse": nurse,
        "id": nurse_id
    }
    return render(request, "admin_template/edit_nurse_template.html", context)


def edit_nurse_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        nurse_id = request.POST.get('nurse_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        special = request.POST.get('special')
        
         # Check if a new profile picture is uploaded
        if request.FILES.get('profile_pic'):
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None

        try:
            # INSERTING into Customuser Model
            user = CustomUser.objects.get(id=nurse_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()
            
            # INSERTING into nurse Model
            nurse_model = Nurse.objects.get(admin=nurse_id)
            nurse_model.address = address
            nurse_model.mobile = mobile
            nurse_model.special = special
            nurse_model.save()
            
            if profile_pic_url:
                nurse_model.profile_pic = profile_pic_url  # Update the profile_pic field

            nurse_model.save()

            messages.success(request, "Nurse Updated Successfully.")
            return redirect('/edit_nurse/'+nurse_id)

        except:
            messages.error(request, "Failed to Update nurse.")
            return redirect('/edit_nurse/'+nurse_id)


def delete_nurse(request, nurse_id):
    try:
        user = CustomUser.objects.get(id=nurse_id)
        nurse = user.nurse
        user.delete()  # Delete the CustomUser objects
        nurse.delete()  # Delete the associated Nurse objects
        messages.success(request, "Nurse deleted successfully.")
        return redirect('manage_nurse')
    except CustomUser.DoesNotExist:
        messages.error(request, "Nurse does not exist.")
    except Exception as e:
        messages.error(request, f"Failed to delete nurse: {str(e)}")
    return redirect('manage_nurse')   

    return redirect('manage_nurse')
    
    
###Doctor Views
def doctor_home(request):
    return render(request, "doctor_template/doctor_home_template.html")

def registration_clerk(request):
    return render(request, "admin_template/registration_clerk_template.html")

def add_registration_clerk(request):
    return render(request, "admin_template/add_registration_clerk_template.html")


def add_registration_clerk_save(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        special = request.POST.get('special')
        
        profile_pic = request.FILES.get('profile_pic')

        if profile_pic:
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = filename
        else:
            profile_pic_url = 'profile_pics/default_profile_pic.jpeg'
            
        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=4)
            user.registration_clerk.address = address
            user.registration_clerk.mobile = mobile
            user.registration_clerk.special = special
            user.registration_clerk.profile_pic = profile_pic_url
                
            user.save()
            messages.success(request, "Registration Clerk Added Successfully!")
            return redirect('add_registration_clerk')
        except:
            messages.error(request, "Failed to Add Registration Clerk!")
            return redirect('add_registration_clerk')
        
    else:
        messages.error(request, "Invalid Method ")
        return redirect('add_registration_clerk')



def manage_registration_clerk(request):
    registration_clerks = Registration_clerk.objects.all()
    context = {
        "registration_clerks": registration_clerks
    }
    return render(request, "admin_template/registration_clerk_template.html", context)


def edit_registration_clerk(request, registration_clerk_id):
    registration_clerk = Registration_clerk.objects.get(admin=registration_clerk_id)

    context = {
        "registration_clerk": registration_clerk,
        "id": registration_clerk_id
    }
    return render(request, "admin_template/edit_registration_clerk_template.html", context)


def edit_registration_clerk_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        registration_clerk_id = request.POST.get('registration_clerk_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        special = request.POST.get('special')

        # Check if a new profile picture is uploaded
        if request.FILES.get('profile_pic'):
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None

        try:
            # UPDATE CustomUser model
            user = CustomUser.objects.get(id=registration_clerk_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            # UPDATE registration_clerk model
            registration_clerk_model = Registration_clerk.objects.get(admin=registration_clerk_id)
            registration_clerk_model.address = address
            registration_clerk_model.mobile = mobile
            registration_clerk_model.special = special

            if profile_pic_url:
                registration_clerk_model.profile_pic = profile_pic_url  # Update the profile_pic field

            registration_clerk_model.save()

            messages.success(request, "Registration Clerk Updated Successfully.")
            return redirect('/edit_registration_clerk/'+registration_clerk_id)

        except:
            messages.error(request, "Failed to Update registration clerk.")
            return redirect('/edit_registration_clerk/'+registration_clerk_id)

def delete_registration_clerk(request, registration_clerk_id):
    try:
        user = CustomUser.objects.get(id=registration_clerk_id)
        registration_clerk = user.registration_clerk
        user.delete()  # Delete the CustomUser objects
        registration_clerk.delete()  # Delete the associated registration_clerk objects
        messages.success(request, "registration clerk deleted successfully.")
        return redirect('manage_registration_clerk')
    except CustomUser.DoesNotExist:
        messages.error(request, "registration_clerk does not exist.")
    except Exception as e:
        messages.error(request, f"Failed to delete registration_clerk: {str(e)}")
    return redirect('manage_registration_clerk')



##########################   Accountant Template  ##############################
def accountant_template(request):
    return render(request, 'accountant_template/base_template.html' )


##########################    Laboratorist Template    ##############################
@authenticate_user(user_type='1')
def laboratorist(request):
    lab = Laboratorist.objects.all()
    context ={
        'lab' : lab
    }
    return render(request, "admin_template/laboratorist_template.html", context)

def lab_home(request):
    return render(request, 'laboratorist_template/home_template.html' )

def laboratorist_template(request):
    add_diagnosis = Add_diagnosis.objects.all()
    total_diagnosis = add_diagnosis.count()
    donor_details = Manage_blood_donor.objects.all()
    total_donors = donor_details.count()
    context = {
        'total_donors' : total_donors,
        'total_diagnosis' : total_diagnosis
    }
    return render(request, 'laboratorist_template/home_template.html', context )
    
def add_diagnosis(request):
    return render(request, 'laboratorist_template/add_diagnosis.html' )

def add_diagnosis_report(request):
    report = Add_diagnosis.objects.all()
    context ={
        'report' : report
    }
    return render(request, 'laboratorist_template/add_diagnosis_report.html', context)   

def add_diagnosis_report_save(request):
    if request.method == 'POST':
        patients_name = request.POST.get('patients_name')
        age = request.POST.get('age')
        address = request.POST.get('address')
        sample_taken = request.POST.get('sample_taken')
        findings  = request.POST.get('findings')
        # timetaken = request.POST.get('timetaken')
        # print(sample_taken)
        report = Add_diagnosis.objects.create(
            patients_name = patients_name,
            age = age,
            address = address,
            sample_taken = sample_taken,
            findings = findings,
            # timetaken = timetaken
        )

        report.save()

        messages.success(request, "Added A Laboratory Report Successfully")
        return redirect('add_diagnosis_report')
    else:
        messages.error(request, "Invalid Method!")
        return redirect('add_diagnosis_report')    
    

def edit_diagnosis_report(request, id):
    report = Add_diagnosis.objects.filter(id=id)
    # 
    if request.method == 'POST':
        patients_name = request.POST.get('patients_name')
        age = request.POST.get('age')
        address = request.POST.get('address')
        sample_taken = request.POST.get('sample_taken')
        findings  = request.POST.get('findings')

        try:
            report.update(
                patients_name = patients_name,
                age = age,
                address = address,
                sample_taken = sample_taken,
                findings = findings,
            )
            messages.success(request, 'Successfully updated a Diagnosis Report')
            return redirect ('add_diagnosis_report')
        
        except:
            messages.error(request, 'Failed to update a Diagnosis Report')

    context={
        'report':report.first()
    }
    return render(request, 'laboratorist_template/edit_diagnosis.html', context)

def delete_report(request, id):
    report = Add_diagnosis.objects.get(id=id)
    try:
        report.delete()
        messages.success(request, 'Successfully deleted a Record')
        return redirect(request, 'add_diagnosis')
    except:
        messages.error(request, 'Failed to Delete a Diagnosis Report')
        return redirect(request, 'add_diagnosis')


########################### MANAGE DONOR ############################
def add_donor(request):
    return render(request, 'laboratorist_template/add_donor.html')

def add_donor_report(request):
    donor_details = Manage_blood_donor.objects.all()
    context = {
        'donor_details' : donor_details
    }
    return render(request, 'laboratorist_template/add_donor_report.html', context)

def add_donor_report_save(request):
    if request.method == 'POST':
        donors_name = request.POST.get('donors_name')
        blood_type = request.POST.get('blood_type')
        age = request.POST.get('age')
        weight = request.POST.get('weight')
        mobile = request.POST.get('mobile')
        location = request.POST.get('location')

        print(mobile, location)

        report = Manage_blood_donor.objects.create(
            donors_name = donors_name,
            blood_type = blood_type,
            age = age,
            weight = weight,
            mobile = mobile,
            location = location,
        )
        report.save()

        messages.success(request, "Added A Blood Donors Report Successfully")
        return redirect('add_donor_report')
    else:
        messages.error(request, "Invalid Method!")
        return redirect('add_donor_report')

def edit_donor_report(request, id):
    report = Manage_blood_donor.objects.filter(id=id)
    # 
    if request.method == 'POST':
        donors_name = request.POST.get('donors_name')
        age = request.POST.get('age')
        weight = request.POST.get('weight')
        blood_type = request.POST.get('blood_type')
        mobile = request.POST.get('mobile')
        location = request.POST.get('location')

        try:
            report.update(
                donors_name = donors_name,
                age = age,
                weight = weight,
                blood_type = blood_type,
                mobile = mobile,
                location = location
            )
            messages.success(request, 'Successfully updated a donor')
            return redirect ('add_donor_report')
        
        except:
            messages.error(request, 'Failed to update a donor')

    context={
        'report':report.first()
    }
    return render(request, 'laboratorist_template/edit_donor.html', context)

def delete_donor(request, id):
    report = Manage_blood_donor.objects.get(id=id)
    try:
        report.delete()
        messages.success(request, "Donor Deleted Successfully.")
        return redirect('add_donor_report')
    except:
        messages.error(request, "Failed to Delete Donor.")
        return redirect('add_donor_report')
    
def blood_bank(request):
    report = Manage_blood_donor.objects.all()
    type_1 = Manage_blood_donor.objects.filter(blood_type='A+').count()
    type_2 = Manage_blood_donor.objects.filter(blood_type='A-').count()
    type_3 = Manage_blood_donor.objects.filter(blood_type='B+').count()
    type_4 = Manage_blood_donor.objects.filter(blood_type='B-').count()
    type_5 = Manage_blood_donor.objects.filter(blood_type='AB+').count()
    type_6 = Manage_blood_donor.objects.filter(blood_type='AB-').count()
    type_7 = Manage_blood_donor.objects.filter(blood_type='O+').count()
    type_8 = Manage_blood_donor.objects.filter(blood_type='O-').count()

    total = Manage_blood_donor.objects.all().count()

    context ={
        'report':report,
        'type_1' : type_1,
        'type_2' : type_2,
        'type_3' : type_3,
        'type_4' : type_4,
        'type_5' : type_5,
        'type_6' : type_6,
        'type_7' : type_7,
        'type_8' : type_8,
        'total':total
    }
    return render(request, 'laboratorist_template/blood_bank.html', context)

##########################  Registration Clerk Template #############################

@authenticate_user(user_type='4')
def registration_clerk_home(request):
    return render(request, "registration_clerk_template/registration_clerk_home_template.html")

def registration_clerk_profile(request):
    return render(request, "registration_clerk_template/registration_clerk_profile.html")

@authenticate_user(user_type='4')
def registration_clerk_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    registration_clerk = Registration_clerk.objects.get(admin=user)
    return render(request, "registration_clerk_template/registration_clerk_profile.html", {"user":user, "registration_clerk":registration_clerk})

def edit_registration_clerk_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    registration_clerk = Registration_clerk.objects.get(admin=user)

    return render(request, "registration_clerk_template/edit_registration_clerk_profile.html", {"user": user, "registration_clerk": registration_clerk})

def submit_registration_clerk_profile(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('registration_clerk_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        profile_pic = request.FILES.get('profile_pic')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            
            registration_clerk = Registration_clerk.objects.get(admin=customuser.id)
            registration_clerk.mobile = mobile
            registration_clerk.address = address
            
            # Check if a new profile picture was uploaded
            if profile_pic:
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                registration_clerk.profile_pic = filename
            
            registration_clerk.save()
            
            messages.success(request, "Profile Updated Successfully")
            return redirect('edit_registration_clerk_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('edit_registration_clerk_profile')
        
def register_patient(request):
    return render(request, "registration_clerk_template/register_patient_template.html")

def register_patient_save(request):
    if request.method == "POST":
        # Retrieve form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile = request.POST.get('mobile')
        gender = request.POST.get('gender')
        condition = request.POST.get('condition')
        category = request.POST.get('category')
        date_of_birth = request.POST.get('date_of_birth')
        address = request.POST.get('address')
        height = request.POST.get('height')
        weight = request.POST.get('weight')

        # Convert date_of_birth to a datetime object
        date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()

        # Create a new PatientRegistration instance and save it
        try:
            registered_patient = PatientRegistration.objects.create(
                first_name=first_name,
                last_name=last_name,
                mobile=mobile,
                gender=gender,
                condition=condition,
                category=category,
                date_of_birth=date_of_birth,
                address=address,
                height=height,
                weight=weight,
            )
        
            messages.success(request, "Patient Registered Successfully")
            return redirect('register_patient')

        except Exception as e:
            messages.error(request, f"Failed to Register Patient: {str(e)}")
            return redirect('register_patient')

    else:
        messages.error(request, "Invalid Method")
        return redirect('register_patient')


def registered_patient_list(request):
    registered_patients = PatientRegistration.objects.all()
    today = date.today()

    # Calculate age for each patient and update their age attribute
    for patient in registered_patients:
        patient.age = today.year - patient.date_of_birth.year - ((today.month, today.day) < (patient.date_of_birth.month, patient.date_of_birth.day))

    return render(request, 'registration_clerk_template/registered_patient_list.html', {'registered_patients': registered_patients})


def registered_patient_details(request, registered_patient_id):
    registered_patient = get_object_or_404(PatientRegistration, pk=registered_patient_id)

    # Calculate the age for the patient
    today = date.today()
    registered_patient.age = today.year - registered_patient.date_of_birth.year - ((today.month, today.day) < (registered_patient.date_of_birth.month, registered_patient.date_of_birth.day))
    
    if registered_patient.height and registered_patient.weight:
        bmi = registered_patient.weight / (registered_patient.height * registered_patient.height)
        bmi = round(bmi, 2)
    else:
        bmi = None

    # Add the calculated BMI to the patient object
    registered_patient.bmi = bmi

    return render(request, 'registration_clerk_template/registered_patient_details.html', {'registered_patient': registered_patient})


def generate_pdf(request, registered_patient_id):
    registered_patient = get_object_or_404(PatientRegistration, pk=registered_patient_id)

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()


    elements = []
    
   

     # Add the hospital name and contact information
    hospital_name = "TIBA Hospital"
    hospital_email = "tiba@gmail.com"
    hospital_contact = "123-456-7890"

    # Create a Paragraph with center alignment for the hospital information
    hospital_info = f"<b>{hospital_name}</b><br/>{hospital_email}<br/>{hospital_contact}"
    header = Paragraph(hospital_info, styles['Normal'])
    header.alignment = 1  # 0=left, 1=center, 2=right
    elements.append(header)

    # Add some space above the hospital information
    elements.append(Spacer(1, 30))
    
    
    # Add patient details to the PDF
    table_data = [
        ["First Name:", "Last Name:",  "Gender:", "Address:", "Mobile:", "Date of Birth:", "Patient Type: " ],
        [registered_patient.first_name, registered_patient.last_name, registered_patient.gender, registered_patient.address,registered_patient.mobile, registered_patient.date_of_birth, registered_patient.patient_type],
        # Add other patient details here
        #["BMI:", registered_patient.bmi],  # Assuming you've calculated the BMI in the view
    ]

    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    table = Table(table_data)
    table.setStyle(table_style)
    elements.append(table)

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()

     # Create an HttpResponse with the PDF as content and 'application/pdf' as content type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{registered_patient.first_name}_{registered_patient.last_name}_details.pdf"'
    response.write(pdf)

    return response

def edit_registered_patient(request, registered_patient_id):
    registered_patient = get_object_or_404(PatientRegistration, id=registered_patient_id)

    context = {
        "registered_patient": registered_patient,
        "id": registered_patient_id
    }
    return render(request, "registration_clerk_template/edit_registered_patient.html", context)

def edit_registered_patient_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        registered_patient_id = request.POST.get('registered_patient_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        mobile = request.POST.get('mobile')
        date_of_birth = request.POST.get('date_of_birth')
        patient_type = request.POST.get('patient_type')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        category = request.POST.get('category')
        condition = request.POST.get('condition')
        address = request.POST.get('address')

        try:
            # UPDATE PatientRegistration model
            registered_patient_model = get_object_or_404(PatientRegistration, id=registered_patient_id)
            registered_patient_model.first_name = first_name
            registered_patient_model.last_name = last_name
            registered_patient_model.gender = gender
            registered_patient_model.mobile = mobile
            registered_patient_model.date_of_birth = date_of_birth
            registered_patient_model.patient_type = patient_type
            registered_patient_model.height = height
            registered_patient_model.weight = weight
            registered_patient_model.category = category
            registered_patient_model.condition = condition
            registered_patient_model.address = address
        
            registered_patient_model.save()

            messages.success(request, "Patient Updated Successfully.")
        except Http404:
            messages.error(request, "Patient with the given ID does not exist.")
        except:
            messages.error(request, "Failed to Update Patient.")

    return redirect('edit_registered_patient', registered_patient_id=registered_patient_id)


def delete_registered_patient(request, registered_patient_id):
    try:
        registered_patient = get_object_or_404(PatientRegistration, id=registered_patient_id)
        registered_patient.delete()  # Delete the PatientRegistration object
        messages.success(request, "Registered Patient deleted successfully.")
    except Exception as e:
        messages.error(request, f"Failed to delete Registered Patient: {str(e)}")
    
    return redirect('registered_patient_list')

@authenticate_user(user_type='4')
def book_appointment(request, registered_patient_id):
    if request.method == "POST":
        doctor_id = request.POST.get('doctor_id')
        date = request.POST.get('date')
        time = request.POST.get('time')

        try:
            registered_patient = PatientRegistration.objects.get(id=registered_patient_id)
            doctor = Doctor.objects.get(id=doctor_id)

            # Get the currently logged-in registration clerk
            registration_clerk = request.user.registration_clerk

            # Create the appointment object and save it to the database
            appointment = Appointment.objects.create(doctor=doctor, registered_patient=registered_patient, registration_clerk=registration_clerk, date=date, time=time)
            appointment.save()

            messages.success(request, "Appointment Made Successfully!")
            return redirect('manage_appointment')  # Replace 'success_page' with the URL name of the success page

        except PatientRegistration.DoesNotExist:
            messages.error(request, "Failed! Patient Does Not Exist")
            return redirect('book_appointment') 

        except Doctor.DoesNotExist:
            messages.error(request, "Falied! Doctor Does Not Exist")
            return redirect('book_appointment')

    else:
        registered_patient = PatientRegistration.objects.get(id=registered_patient_id)
        doctors = Doctor.objects.all()
        context = {
            'registered_patient': registered_patient,
            'doctors': doctors,
        }
        return render(request, 'registration_clerk_template/book_appointment.html', context)
        
        
def manage_appointment(request):
    appointments = Appointment.objects.all()
    messages.get_messages(request)
    return render(request, 'registration_clerk_template/manage_appointment.html', {'appointments': appointments})


def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    doctors = Doctor.objects.all()  # Retrieve all doctors from the database

    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')
        date = request.POST.get('date')
        time = request.POST.get('time')

        doctor = Doctor.objects.get(id=doctor_id)  # Retrieve the doctor object using the doctor_id

        appointment.doctor = doctor  
        appointment.date = date
        appointment.time = time

        appointment.save()
        return redirect('manage_appointment')

    context = {
        'appointment': appointment,
        'doctors': doctors,  # Pass the doctors queryset to the template context
    }

    return render(request, 'registration_clerk_template/edit_appointment.html', context)



def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == 'POST':
        confirm = request.POST.get('confirm')
        if confirm == 'yes':
            try:
                appointment.delete()
                messages.success(request, 'Appointment was canceled successfully.')
            except Exception as e:
                messages.error(request, 'Failed to cancel the appointment: {}'.format(str(e)))

            return redirect('manage_appointment')

    return render(request, 'registration_clerk_template/cancel_appointment.html', {'appointment': appointment})




############################  SETTINGS  #######################
def laboratorist_settings(request):
    return render(request, 'laboratorist_template/settings.html', )

def doctor_settings(request):
    return render(request, 'doctor_template/settings.html', )

def testmail(request):
    send_mail(
        "Testing",
        "Testing email",
        "console",
        ["collinsotieno380@gmail.com"],
        fail_silently=True
    )

    return HttpResponse({"test":"done"})