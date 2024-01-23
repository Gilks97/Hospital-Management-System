from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField
from django.core.validators import RegexValidator
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class DateInput(forms.DateInput):
    input_type = 'date'
 
class InputTime(forms.TimeInput):
    input_type='time'

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'category_name': forms.Select(attrs={'class': 'form-control'}),
            'item_name': forms.TextInput(attrs={'class': 'form-control'}),
            'item': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class StockForm(forms.ModelForm):
    class Meta:
        model = SalesInvoice
        fields = ['item',   'expiry_date', 'date_bought','sold','bought']
        widgets = {
            'item': forms.TextInput(attrs={'class': 'form-control'}),
           
           
            'bought': forms.NumberInput(attrs={'class': 'form-control'}),
            'sold': forms.NumberInput(attrs={'class': 'form-control'}),
          
            'expiry_date':DateInput(attrs={'class': 'form-control'}),
            'date_bought':DateInput(attrs={'class': 'form-control'}),
        }
class MedicineForm(forms.ModelForm):  
  class Meta:
      model=Ordering  
      fields=['quantity' ] 
      widgets={
          'total_quantity': forms.NumberInput(attrs={'class': 'form-control'}) 
      }
    
class Sendinmail(forms.Form):
    subject = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    reciever = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    message = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))

class CartForm(forms.ModelForm):
    class Meta:
        model=CartItem
        fields=['quantity']

# class PharmacistRegistrationForm(UserCreationForm):
#     first_name=forms.CharField(max_length=100)
#     last_name=forms.CharField(max_length=100)
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'email','first_name','last_name', 'password1','password2']
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
#             'first_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'last_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'address': forms.TextInput(attrs={'class': 'form-control'}),
#             'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
# #             'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
#         }
class PatientPicForm1(forms.ModelForm):
    class Meta:
        model=Patient
        fields='__all__'
        exclude=['admin','gender','mobile','address','dob']
class DealerForm(forms.ModelForm):
    class Meta:
        model=Dealer
        fields='__all__'
        widgets= {
            'dmame': forms.TextInput(attrs={'class': 'form-control','placeholder':'full name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phn_no': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DealerContactForm(forms.ModelForm):
   class Meta:
       model=Dealermessage
       fields=['subject','message']
       widget={
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control'}),
       }
       
class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = '__all__'
        widgets = {
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'patientname': forms.Select(attrs={'class': 'form-control'}),
            'prescription': forms.Textarea(attrs={'class': 'form-control'}),
            'medicine': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

class DispenseForm(forms.ModelForm):
    dispense_date = forms.DateField(widget=DateInput(attrs={'class': 'form-control'}))
    dispense_time = forms.TimeField(widget=InputTime(attrs={'class': 'form-control'}))

    class Meta:
        model = Dispense
        fields = '__all__'
        widgets = {
            'dispense': forms.Select(attrs={'class': 'form-control'}),
            'medicine': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'taken': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control'}),
        }


class PharmacistForm(forms.ModelForm):
    class Meta:
        model=Pharmacist
        fields='__all__'
        exclude=['admin','gender','mobile','address']


class PatientForm(forms.Form):

    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    reg_no = forms.CharField(label="Reg No", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    phone_number = forms.CharField(label="Mobile", max_length=50)
    gender_list = (
        ('Male','Male'),
        ('Female','Female')
    )
    gender = forms.ChoiceField(label="Gender", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    dob= forms.DateField(label="dob", widget=DateInput(attrs={"class":"form-control"}))

    # Validations for patient
    def clean_reg_no(self):
        reg_no = self.cleaned_data['reg_no']
        if  not  reg_no:
            raise ValidationError("This field is required")
        for instance in Patient.objects.all():
            if instance.reg_no==reg_no:
                raise ValidationError( "Registration number aready exist")
      
        return reg_no


    def clean_phone_number(self):
        phone_number=self.cleaned_data.get('phone_number')
        if not phone_number:
            raise forms.ValidationError('This field is requied')
        elif len(phone_number) < 10:
            raise forms.ValidationError('Invalid Number')
        for instance in Patient.objects.all():
            if instance.phone_number==phone_number:
                raise ValidationError( "PhoneNumber aready exist")
        
        return phone_number
        
            
   
    def clean_username(self):
        username = self.cleaned_data['username']
        if  not  username:
            raise ValidationError("This field is required")
        for instance in CustomUser.objects.all():
            if instance.username==username:
                raise ValidationError( "Username aready exist")
      
        return username

    def clean_firstName(self):
        first_name = self.cleaned_data['first_name']
        if  not  first_name:
            raise ValidationError("This field is required")
        return first_name

    def clean_secondName(self):
        last_name = self.cleaned_data['last_name']
        if  not  last_name:
            raise ValidationError("This field is required")
        return last_name

class EditPatientForm(forms.Form):
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    phone_number = forms.CharField(label="Mobile", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    gender_list = (
        ('Male','Male'),
        ('Female','Female')
    )
    gender = forms.ChoiceField(label="Gender", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    dob= forms.DateField(label="dob", widget=DateInput(attrs={"class":"form-control"}))

class PatientSearchForm1(forms.ModelForm):
    
    class Meta:
        model=Patient
        fields='__all__'
        exclude=['profile_pic','gender','mobile','address','dob']
class PatientForm7(forms.ModelForm):
     class Meta:
        model=Patient
        fields='__all__'           