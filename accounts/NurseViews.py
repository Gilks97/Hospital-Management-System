from django.shortcuts import redirect, render
from django.contrib import messages
from accounts.models import CustomUser, Nurse
from .decorators import authenticate_user
from django.core.files.storage import FileSystemStorage



@authenticate_user(user_type='3')
def nurse_home(request):
    return render(request, "nurse_template/nurse_home_template.html")

def nurse_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    nurse = Nurse.objects.get(admin=user)
    return render(request, "nurse_template/nurse_profile.html", {"user":user, "nurse":nurse})

def edit_nurse_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    nurse = Nurse.objects.get(admin=user)

    return render(request, "nurse_template/edit_nurse_profile.html", {"user": user, "nurse": nurse})

def submit_nurse_profile(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('nurse_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        specialization = request.POST.get('specialization')
        profile_pic = request.FILES.get('profile_pic')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            
            nurse = Nurse.objects.get(admin=customuser.id)
            nurse.mobile = mobile
            nurse.address = address
            nurse.specialization = specialization
            
             # Check if a new profile picture was uploaded
            if profile_pic:
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                nurse.profile_pic = filename
            
            nurse.save()
            
            messages.success(request, "Profile Updated Successfully")
            return redirect('edit_nurse_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('edit_nurse_profile')