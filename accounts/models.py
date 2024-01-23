from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.timezone import now
import uuid
from django.db.models.signals import pre_save,post_save
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.db.models import BooleanField, ExpressionWrapper, Q
from django.db.models.functions import Now
import uuid

class CustomUser(AbstractUser):
    user_type_data = ((1, "AdminHims"), (2, "Doctor"), (3, "Nurse"), (4, "Registration_clerk"), (5, "Patient"), (6, 'Laboratorist'),(7,'Pharmacist'))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=20)
    reset_password_token = models.CharField(max_length=100, null=True, blank=True)  # Add this field

class AdminHims(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE,default=None)
    profile_pic = models.FileField(upload_to='profile_pics/', default='default_profile_pic.jpeg')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Doctor(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, default=None)
    address = models.TextField()
    profile_pic = models.FileField(upload_to='profile_pics/', default='default_profile_pic.jpeg')
    mobile = models.CharField(max_length=20)  # Updated field to CharField
    special = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    
    def __str__(self):
        user = self.admin 
        return f"Dr. {user.get_full_name()}"
    
class Nurse(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE,default=None) 
    address=models.TextField()
    profile_pic = models.FileField(upload_to='profile_pics/', default='default_profile_pic.jpeg')
    mobile = models.CharField(max_length=20)
    specialization = models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
    
class Registration_clerk(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE,default=None)
    address=models.TextField()
    profile_pic = models.FileField(upload_to='profile_pics/', default='default_profile_pic.jpeg')
    mobile = models.CharField(max_length=20)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
    
class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, default=None)
    mobile = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    profile_pic = models.FileField(upload_to='profile_pics/', default='default_profile_pic.jpeg')
    condition = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Pharmacist(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE,default=None) 
    address=models.TextField()
    profile_pic = models.FileField(upload_to='profile_pics/', default='default_profile_pic.jpeg')
    mobile = models.CharField(max_length=20)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
    
class PatientRegistration(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    mobile = models.CharField(max_length=20)
    address = models.TextField()
    patient_type = models.CharField(max_length=10, default='Outpatient')
    condition = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    height = models.DecimalField(max_digits=5, decimal_places=2)  
    weight = models.DecimalField(max_digits=5, decimal_places=2)  
    def calculate_age(self):
        today = date.today()
        age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return age
    
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('in_treatment', 'In Treatment'),
        ('in_pharmacy', 'In Pharmacy'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    objects = models.Manager()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    
class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    registration_clerk = models.ForeignKey(Registration_clerk, on_delete=models.CASCADE, default=None)
    date = models.DateField()
    time = models.TimeField()

    # Define the foreign key relationships for the patient and registered patient
    # Use 'null=True' and 'blank=True' to make these fields optional
    # This allows an appointment to be associated with either a regular patient or a registered patient, or both
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    registered_patient = models.ForeignKey(PatientRegistration, on_delete=models.CASCADE, null=True, blank=True)

    # Define the __str__ method to provide a human-readable representation of the appointment
    def __str__(self):
        # Check if the appointment has a patient or a registered patient, and return the corresponding string representation
        if self.patient:
            return f"{self.patient} - {self.doctor} - {self.date} {self.time}"
        elif self.registered_patient:
            return f"{self.registered_patient} - {self.doctor} - {self.date} {self.time}"
        else:
            # If neither patient nor registered patient is assigned, return a generic string representation
            return f"Appointment - {self.doctor} - {self.date} {self.time}"

    objects = models.Manager()
    
class Departments(models.Model):
    id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=255, null=True, blank=True)  # Updated field
    department_description = models.CharField(max_length=255, null=True, blank=True)
    objects = models.Manager()
    

def __str__(self):
        return self.department_name

    
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            AdminHims.objects.create(admin=instance)
        if instance.user_type==2:
            Doctor.objects.create(admin=instance)
        if instance.user_type==3:
            Nurse.objects.create(admin=instance)
        if instance.user_type==4:
            Registration_clerk.objects.create(admin=instance)
        if instance.user_type==5:
            Patient.objects.create(admin=instance,
            mobile=0,
            gender="",
            address="",
            condition="",
            category="",
            date_of_birth="2000-01-01",
            age=0)
        if instance.user_type==6:
            Laboratorist.objects.create(admin=instance)
        if instance.user_type==7:
            Pharmacist.objects.create(admin=instance)    
        
            
@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhims.save()
    if instance.user_type == 2:
        instance.doctor.save()
    if instance.user_type == 3:
        instance.nurse.save()
    if instance.user_type == 4:
        instance.registration_clerk.save()
    if instance.user_type == 5:
        instance.patient.save()
    if instance.user_type == 6:
        instance.laboratorist.save()
    if instance.user_type == 7:
        instance.pharmacist.save()        


class Laboratorist(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE,default=None)
    address=models.TextField()
    profile_pic = models.FileField(upload_to='profile_pics/', default='default.png')
    mobile = models.CharField(max_length=20)
    specialty = models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Add_diagnosis(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4)
    patients_name = models.CharField(max_length=200)
    age = models.CharField(max_length=10)
    address = models.CharField(max_length=70)
    sample_taken = models.CharField(max_length=100)
    findings = models.TextField()
    timetaken = models.DateTimeField(auto_now_add=True)


class Manage_blood_donor(models.Model):

    b_type = (
    ('A+', 1),
    ('A-', 2),
    ('B+', 3),
    ('B-', 4),
    ('AB+', 5),
    ('AB-', 6),
    ('O+', 7),
    ('O-', 8),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    donors_name = models.CharField(max_length=150)
    age = models.CharField(max_length=4)
    weight = models.CharField(max_length=5)
    blood_type = models.CharField(choices=b_type, max_length=3, null=False)
    mobile = models.CharField(max_length=10)
    location = models.CharField(max_length=100)
    date_taken = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name 

class Product(models.Model):
    
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=50, null=True, blank=True)
    item = models.ImageField(upload_to='images/items', blank=False, null=False)
    unit_price = models.IntegerField(default=0)
    sold=models.IntegerField(default=0)
    def __str__(self):
        return self.item_name
      
class SalesInvoice(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    item=models.CharField(max_length=20)
    bought=models.IntegerField(default=1)    
    sold = models.PositiveIntegerField(default=0)
    expiry_date = models.DateField(null=False)
    date_bought = models.DateField(null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Sale #{self.pk}"      
    @property
    def items_available(self):
        return self.bought - self.sold 
    @property
    def expired(self):
        if self.expiry_date <= now().date():
            return self.items_available
        else:
            return 0

      

class Ordering(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    def __int__(self):
        return  self.pk
    
class Cart(models.Model):
    id=models.UUIDField(default=uuid.uuid4,primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  
    order=models.BooleanField(default=False)  
    def __str__(self): 
        return str(self.id)    
    @property
    def total_price(self):
        allitems=self.cartitema.all()
        total=sum([ item.price for item in allitems ])
        return total    
    @property
    def num_items(self):
        general=self.cartitema.all()
        quantity=sum([item.quantity for item in general])
        return quantity


class CartItem (models.Model):     
    product= models.ForeignKey(Product,on_delete=models.CASCADE,related_name='citem')
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE,related_name='cartitema')
    quantity=models.IntegerField(default=0)
    def __str__(self):
        return self.product.item_name    
    @property  #making it a field
    def price(self):
        new_price=self.product.unit_price * self.quantity 
        return new_price

class Notification(models.Model):
    sale_invoice = models.ForeignKey(SalesInvoice, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Dealer(models.Model):
    dname = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    phn_no = models.BigIntegerField(unique=True)
    email = models.EmailField(max_length=50)

    def __str__(self):
        return self.email
    
class Dealermessage(models.Model):
    subject=models.CharField(max_length=30)
    message=models.TextField()
    user= models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    
class Prescription(models.Model):
    patient_id = models.ForeignKey(Patient,null=True, on_delete=models.SET_NULL)
    description=models.TextField(null=True)
    prescribe=models.CharField(max_length=100,null=True)
    date_precribed=models.DateTimeField(auto_now_add=True, auto_now=False)

class Dispense(models.Model):
    dispense=models.ForeignKey(Prescription,on_delete=models.CASCADE ,related_name='precribed')    
    medicine=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='items1')
    quantity=models.IntegerField(default='1')
    instructions=models.TextField(max_length=300,null=True, blank=False)
    dispense_date = models.DateField()
    dispense_time = models.TimeField(auto_now_add=True)  
    remarks = models.TextField(blank=True, null=True)
    taken = models.BooleanField(default=False) 

class ExpiredManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(
            expired=ExpressionWrapper(Q(valid_to__lt=Now()), output_field=BooleanField())
        )

class PatientFeedback(models.Model):
    id = models.AutoField(primary_key=True)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    admin_id= models.ForeignKey( AdminHims,null=True, on_delete=models.CASCADE)
    pharmacist_id=models.ForeignKey( Pharmacist,null=True, on_delete=models.CASCADE)
    feedback = models.TextField(null=True)
    feedback_reply = models.TextField(null=True)
    admin_created_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

# class Dispense(models.Model):
#     patient_id = models.ForeignKey(Patient, on_delete=models.DO_NOTHING,null=True)
#     drug_id = models.ForeignKey(SalesInvoice, on_delete=models.SET_NULL,null=True,blank=False)
#     dispense_quantity = models.PositiveIntegerField(default='1', blank=False, null=True)
#     taken=models.CharField(max_length=300,null=True, blank=True)
#     instructions=models.TextField(max_length=300,null=True, blank=False)
#     dispense_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)

# class C2BTransaction(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     transaction_id = models.CharField(max_length=100)
#     transaction_time = models.DateTimeField(auto_now_add=True)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f"{self.user}'s C2B transaction of {self.amount} at {self.transaction_time}"

# # STATUS = ((1, "Pending"), (0, "Complete"))

# # class Transaction(models.Model):
# #     """This model records all the mpesa payment transactions"""
# #     transaction_no = models.CharField(default=uuid.uuid4, max_length=50, unique=True)
# #     phone_number = PhoneNumberField(null=False, blank=False)
# #     checkout_request_id = models.CharField(max_length=200)
# #     reference = models.CharField(max_length=40, blank=True)
# #     description = models.TextField(null=True, blank=True)
# #     amount = models.CharField(max_length=10)
# #     status = models.CharField(max_length=15, choices=STATUS, default=1)
# #     receipt_no = models.CharField(max_length=200, blank=True, null=True)
# #     created = models.DateTimeField(auto_now_add=True)
# #     ip = models.CharField(max_length=200, blank=True, null=True)

# #     def __unicode__(self):
# #         return f"{self.transaction_no}"
# # class BaseModel(models.Model):
# #     created_at = models.DateTimeField(auto_now_add=True)
# #     updated_at = models.DateTimeField(auto_now=True)
# #     class Meta:
# #         abstract = True
# # # M-pesa Payment models
# # class MpesaCalls(BaseModel):
# #     ip_address = models.TextField()
# #     caller = models.TextField()
# #     conversation_id = models.TextField()
# #     content = models.TextField()
# #     class Meta:
# #         verbose_name = 'Mpesa Call'
# #         verbose_name_plural = 'Mpesa Calls'
# # class MpesaCallBacks(BaseModel):
# #     ip_address = models.TextField()
# #     caller = models.TextField()
# #     conversation_id = models.TextField()
# #     content = models.TextField()
# #     class Meta:
# #         verbose_name = 'Mpesa Call Back'
# #         verbose_name_plural = 'Mpesa Call Backs'
# # class MpesaPayment(BaseModel):
# #     amount = models.DecimalField(max_digits=10, decimal_places=2)
# #     description = models.TextField()
# #     type = models.TextField()
# #     reference = models.TextField()
# #     first_name = models.CharField(max_length=100)
# #     middle_name = models.CharField(max_length=100)
# #     last_name = models.CharField(max_length=100)
# #     phone_number = models.TextField()
# #     organization_balance = models.DecimalField(max_digits=10, decimal_places=2)
# #     class Meta:
# #         verbose_name = 'Mpesa Payment'
# #         verbose_name_plural = 'Mpesa Payments'
# #     def __str__(self):
# #         return self.first_name
  
# # # @receiver(post_save,sender=SalesInvoice)
# # # def check_notifications(sender, instance, **kwargs):
# # #     if instance.expired > 0:
# # #         # Create a new notification for expired items
# # #         message = f"Warning: {instance.expired} items in sale #{instance.pk} have expired."
# # #         notification = Notification(sale_invoice=instance, message=message)
# # #         notification.save()
# # #     elif instance.items_available < 10:
# # #         # Create a new notification for low inventory
# # #         message = f"Warning: only {instance.items_available} items left in stock for sale #{instance.pk}."
# # #         notification = Notification(sale_invoice=instance, message=message)
# # #         notification.save()

# # # Connect the check_notifications function to the post_save signal of the SalesInvoice model
# # # post_save.connect(check_notifications, sender=SalesInvoice)
