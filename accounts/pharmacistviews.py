from django.shortcuts import render
from django.core.mail import send_mail,EmailMessage
from django.conf import settings
from django.contrib.auth.decorators import login_required,user_passes_test
from django.shortcuts import render, redirect,get_object_or_404
from .models import  *
from  .forms import *
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from .forgot import send_forgot_password_mail
import uuid
def admin_check(user):
    return user.user_type=='7'

@login_required
def create_admin_pharmacy_profile(request):
    user=request.user
    if request.method=="POST":
        prof=PharmacistForm(request.POST,request.FILES)
        if prof.is_valid():
            admin_profile = prof.save(commit=False)
            admin_profile.user = user  # Assign the user instance
            admin_profile.save()
            return redirect('admin')
    else:
        prof=PharmacistForm()
    return render(request,'dashboard/admin/create_admin_profile.html',{'form':prof})    
@login_required
def admin_pharmacy_profile(request):
    use= request.user
    try:
        profile = Pharmacist.objects.get(user=use)
    except Pharmacist.DoesNotExist:
        return redirect('create_admin_pharmacy_profile')
    if request.method == 'POST':
        form = PharmacistForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
             form.save()
            
             return redirect('admin')
    else:
        form = PharmacistForm(instance=profile)

    context = {
        'form': form,
        #,
    }
    return render(request, 'dashboard/admin/admin_profile.html', context)


@login_required
@user_passes_test(admin_check)
def product_list(request):
    # #profile = Pharmacist.objects.get(user=request.user) 
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

# @login_required
# def customer_dashboard(request):
#     if request.user.role =='customer':
#      profile = CustomerProfile.objects.get(user=request.user)
#      products = Product.objects.all()
#      product_count=Product.objects.all().count()

#      context= {'products': products,
#                'drugs_count':product_count,
#                'cart':cart,
#                'profile':profile
#                }
#     else:
#        messages.error(request,'not accessible by the user')
#        return redirect('login')
#     return render(request, 'dashboard/customer/customer_dash.html',context)

@login_required
def pharmacist_dashboard(request):
    if request.user.role != 'pharma':
       messages.error(request,'not accessible by the user')
    return render(request, 'dashboard/pharma/pharma_dash.html')

@login_required
@user_passes_test(admin_check)
def admin_dashboard(request):
    # #profile = Pharmacist.objects.get(user=request.user)
    if request.user.user_type=='7':
     products = Product.objects.all()
     product_count=Product.objects.all().count()
     context= {'products': products,
               'drugs_count':product_count,
                #
               }
    else:
       messages.error(request,'not accessible by the user')
       return redirect('login')
    return render(request, 'dashboard/admin/admin_dash.html',context)
   
@login_required
@user_passes_test(admin_check)
def product_list(request):
 #profile = Pharmacist.objects.get(user=request.user)
 drug=Product.objects.all()
 return render(request,'dashboard/admin/product_list.html',{'drugs':drug})    

@login_required
@user_passes_test(admin_check)
def edit_product(request,id):
    drug=Product.objects.get(id=id)
    # #profile = Pharmacist.objects.get(user=request.user)    
    if request.method=='POST':
        prod=ProductForm(request.POST,request.FILES,instance=drug)
        if prod.is_valid():
            prod.save()
            messages.success(request,'product edited succesfully')
            return redirect('product_list')
        else:
            messages.error('missing fields')   
    else:
          prod=ProductForm(instance=drug)     
    return render(request,'dashboard/admin/edit_product.html',{'product':prod})

@login_required
@user_passes_test(admin_check)
def category(request):
    categories=Category.objects.all()
    # #profile = Pharmacist.objects.get(user=request.user) 
    if request.method=='POST': 
        cat=CategoryForm(request.POST)
        if cat.is_valid():
            cat.save()
            return redirect('admin')
    else:
        cat=CategoryForm()
    return render(request,'dashboard/admin/category.html',{'cat':cat,'categs':categories})     
   
@login_required
@user_passes_test(admin_check)
def create_product(request):
    # #profile = Pharmacist.objects.get(user=request.user) 
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully.')
            return redirect('product_list')
        else:
            messages.error(request, 'Missing fields.')
    else:
        form = ProductForm()
    return render(request, 'dashboard/admin/create_product.html', {'form': form})

@login_required
@user_passes_test(admin_check)
def delete_product(request,id):
    # #profile = Pharmacist.objects.get(user=request.user) 
    drug=Product.objects.get(id=id)
    if request.method=='POST':
        drug.delete()
        return redirect('product_list')
    return render(request,'dashboard/admin/delete_product.html',{'drug':drug})
@login_required
@user_passes_test(admin_check)
def admin_search(request):
    search_query=request.GET['getdata']
    results=[]
    if search_query:
      results=Product.objects.filter(item_name__icontains=search_query)
    return render(request, 'dashboard/admin/admin_search.html', {'search_query': search_query, 'results': results})  

def customer_search(request):
    search_query=request.GET['getdata']
    results=[]
    if search_query:
      results=Product.objects.filter(item_name__icontains=search_query)
    return render(request, 'dashboard/customer/customer_search.html', {'search_query': search_query, 'results': results})

# def order(request, id):
#     user = request.user
#     prod = Product.objects.get(id=id)
#     ord=Ordering.objects.all()
#     prof=CustomerProfile.objects.get(user=user)
#     if request.method == "POST":
#         drug = MedicineForm(request.POST)
#         if drug.is_valid(): 
#             order=drug.save(commit=False)
#             order.user=user
#             order.product=prod
#             order.total_cost = order.quantity * prod.unit_price
#             order.save()
#     else:
#         drug = MedicineForm()
#     context={'form': drug, 'drugs': prod,'order':ord,
#              'profile':prof
#              }
#     return render(request, 'dashboard/customer/order.html', context)

@login_required
@user_passes_test(admin_check)
def sale_list(request):
    sales = SalesInvoice.objects.all()
    # prof = Pharmacist.objects.get(user=request.user)
    context = {
        # 'profile': prof,
        'sales': sales
    }
    return render(request, 'dashboard/admin/sale_list.html', context)

@login_required
@user_passes_test(admin_check)
def edit_sale(request, id):
    sale = SalesInvoice.objects.get(id=id)
    # prof = Pharmacist.objects.get(user=request.user)
    if request.method == 'POST':
        sale_form = StockForm(request.POST, request.FILES, instance=sale)
        if sale_form.is_valid():
            form = sale_form.save(commit=False)
            form.user = request.user
            form.save()
            messages.success(request, 'Sale successfully edited')
            return redirect('sale_list')
        else:
            messages.error(request, 'Missing fields')
    else:
        sale_form = StockForm(instance=sale)

    context = {
        'sale_form': sale_form,
        # 'profile': prof
    }
    return render(request, 'dashboard/admin/edit_sale.html', context)

@login_required
@user_passes_test(admin_check)
def create_sale(request):
    # prof = Pharmacist.objects.get(user=request.user)
    if request.method == 'POST':
        sale_form = StockForm(request.POST, request.FILES)
        if sale_form.is_valid():
            form = sale_form.save(commit=False)
            form.user = request.user
            form.save()
            messages.success(request, 'Sales successfully created')
            return redirect('sale_list')
        else:
            messages.error(request, 'Missing fields')
    else:
        sale_form = StockForm()

    context = {
        'sale_form': sale_form,
        # 'profile': prof
    }
    return render(request, 'dashboard/admin/create_sale.html', context)

def delete_sale(request, id):
    sale = SalesInvoice.objects.get(id=id)
    # prof = Pharmacist.objects.get(user=request.user)
    if request.method == 'POST':
        sale.delete()
        return redirect('sale_list')

    return render(request, 'dashboard/admin/delete_sale.html', {'sale': sale, 'profile': prof})
def register_pharmacist(request):
    if request.method == 'POST':
        form = PharmacistRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type= '1'
            user.save()
            # AdminProfile.objects.get_or_create(user=user)
            return redirect('show_login')
    else:
        form = PharmacistRegistrationForm()
    return render(request, 'accounts/admin_registration.html', {'form': form})
def dealerlist(request):
    deal=Dealer.objects.all()
    context={
        'dealers':deal
    }
    return render(request,'dashboard/admin/dealer_list.html',context)

def createdealer(request):
    if request.method == 'POST':
        dealer= DealerForm(request.POST)
        if dealer.is_valid():
            dealer.save()
            messages.success(request, 'dealer successfully created')
            return redirect('dealer_list')
        else:
            messages.error(request, 'Missing fields')
    else:
         dealer= DealerForm()
    context = {
        'dealer':dealer
        # 'profile': prof
    }
    return render(request, 'dashboard/admin/create_dealer.html', context)

def editdealer(request,id):
    deal=Dealer.objects.get(id=id)
    if request.method == 'POST':
        dealer= DealerForm(request.POST,instance=deal)
        if dealer.is_valid():
            dealer.save()
            messages.success(request, 'dealer successfully editted')
            return redirect('dealer_list')
        else:
            messages.error(request, 'Missing fields')
    else:
         dealer= DealerForm(instance=deal)
    context = {
        'dealer':dealer
        # 'profile': prof
    }
    return render(request, 'dashboard/admin/edit_dealer.html', context)

def deletedealer(request,id):
    dealer=Dealer.objects.get(id=id)
    dealer.delete()
    return redirect('dealer_list')

def dealermessage(request,id):
    deal=Dealer.objects.get(id=id)
    if request.method=='POST':
        form=DealerContactForm(request.POST)
        if form.is_valid():
            said=form.save(commit=False)
            said.user=request.user
            subject=said.subject
            mess=said.message
            mail_from=settings.EMAIL_HOST_USER
            mail_to=[deal.email]
            send_mail(
                      subject,
                       f'hi {deal.dname} i am {request.user} from tiba,\n\n {mess}',
                      mail_from,
                      mail_to,
                      )
            said.save()
            messages.success(request,'message sent successfully')
            return redirect('dealer_list')
    else:
        form=DealerContactForm()
    return render(request,'dashboard/admin/message.html',{'form':form})    


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

@user_passes_test(admin_check)
def dispense_list(request):
    presc = Prescription.objects.all()
    prescription_data = {}
    for prescription in presc:
        dispenses = prescription.precribed.all()
        prescription_data[prescription] = dispenses
    context = {
          'presc':presc,
        'prescription_data': prescription_data
    }
    return render(request, 'dashboard/admin/dispense_list.html', context)

def dispense(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)

    if request.method == 'POST':
        form = DispenseForm(request.POST)
        if form.is_valid():
            dispense = form.save(commit=False)
            dispense.dispense = prescription
            dispense.save()
            return redirect('dispense_list')  # Redirect to the dispense list view after dispensing

    else:
        form = DispenseForm()

    return render(request, 'dashboard/admin/dispense.html', {'form': form, 'prescription': prescription})

def edit_dispense(request, prescription_id, dispense_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)
    dispense = get_object_or_404(Dispense,id=dispense_id)

    if dispense_id:
        # If dispense_id is provided, get the existing dispense record to edit
        dispense = get_object_or_404(Dispense, id=dispense_id)

    if request.method == 'POST':
        form = DispenseForm(request.POST, instance=dispense)
        if form.is_valid():
            dispense = form.save(commit=False)
            dispense.dispense = prescription
            dispense.save()
            return redirect('dispense_list')  # Redirect to the dispense list view after saving

    else:
        form = DispenseForm(instance=dispense)

    return render(request, 'dashboard/admin/edit_dispense.html', {'form': form, 'prescription': prescription})


def delete_dispense(request, prescription_id, dispense_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)
    dispense = get_object_or_404(Dispense, id=dispense_id)

    if request.method == 'POST':
        dispense.delete()
        return redirect('dispense_list')  # Redirect to the dispense list view after deletion

    return render(request, 'dashboard/admin/delete_dispense.html', {'dispense': dispense, 'prescription': prescription})

def pharmacist_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    pharmacist = Pharmacist.objects.get(admin=user)
    return render(request, "dashboard/admin/pharma_profile.html", {"user":user, "pharma":pharmacist})
    
def edit_pharmacist_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    pharma= Pharmacist.objects.get(admin=user)    
    return render(request, "dashboard/admin/edit_pharma_profile.html", {"user":user, "pharma":pharma})

def submit_pharma_profile(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('pharma_profile')
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
            
            pharma = pharma.objects.get(admin=customuser.id)
            pharma.mobile = mobile
            pharma.address = address
            
            # Check if a new profile picture was uploaded
            if profile_pic:
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                pharma.profile_pic = filename
            
            pharma.save()
            
            messages.success(request, "Profile Updated Successfully")
            return redirect('edit_pharmacist_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('edit_pharmacist_profile')






