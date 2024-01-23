from django.contrib import admin
from django.urls import path, include

from .models import *
from .views import *
from .DoctorViews import *
from .NurseViews import *
from .accountantViews import *
from .laboratoristViews import *
from .pharmacistviews import *
# from accounts import views
from .patient_view  import *
from .DoctorViews import *


from django.contrib.auth import views as auth_views



urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('testemail', testmail, name="testmail"),
    #path('', home, name="home"),
    path('', ShowLoginPage, name="show_login"),
    path('get_user_details/', GetUserDetails, name="get_user_details"),
    path('login_user/', login_user, name="login_user"),
    path('logout_user/', logout_user, name="logout_user"),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset/password_reset.html') , name="password_reset"),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset/password_reset_done.html') , name="password_reset_done"),
    path('password_reset_done/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset/password_reset_confirm.html'), name="password_reset_confirm" ),
    #admin urls

    path('admin_home/', admin_home, name="admin_home"),
    path('department/', department, name="department"),
    path('doctor/', doctor, name="doctor"),
    path('nurse', nurse, name="nurse"),
    path('patient/', patient, name="patient"),
    path('laboratorist/', laboratorist, name="laboratorist"),
   
    path('accountant/', accountant, name="accountant"),
    path('registration_clerk/', registration_clerk, name="registration_clerk"), 
    path('admin_hims_settings/', admin_hims_settings, name="admin_hims_settings"),
    path('admin_hims_profile/', admin_hims_profile, name="admin_hims_profile"),
    path('edit_admin_hims_profile/', edit_admin_hims_profile, name="edit_admin_hims_profile"),
    path('submit_admin_hims_profile/', submit_admin_hims_profile, name="submit_admin_hims_profile"),
    path('add_department/', add_department, name="add_department"),
    path('add_department_save/', add_department_save, name="add_department_save"),
    path('manage_department/', manage_department, name="manage_department"),
    path('edit_department/<int:department_id>/', edit_department, name="edit_department"),
    path('edit_department_save/', edit_department_save, name="edit_department_save"),
    path('delete_department/<department_id>/', delete_department, name="delete_department"),
    path('add_doctor/', add_doctor, name="add_doctor"),
    path('add_doctor_save/', add_doctor_save, name="add_doctor_save"),
    path('manage_doctor/', manage_doctor, name="manage_doctor"),
    path('edit_doctor/<doctor_id>/', edit_doctor, name="edit_doctor"),
    path('edit_doctor_save/', edit_doctor_save, name="edit_doctor_save"),
    path('delete_doctor/<doctor_id>/', delete_doctor, name="delete_doctor"),
    path('add_nurse/', add_nurse, name="add_nurse"),
    path('add_nurse_save/', add_nurse_save, name="add_nurse_save"),
    path('manage_nurse/', manage_nurse, name="manage_nurse"),
    path('edit_nurse/<nurse_id>/', edit_nurse, name="edit_nurse"),
    path('edit_nurse_save/', edit_nurse_save, name="edit_nurse_save"),
    path('delete_nurse/<nurse_id>/', delete_nurse, name="delete_nurse"),
    path('add_pharmacist/', add_pharmacist, name="add_pharmacist"),
    path('add_pharmacist_save/', add_pharmacist_save, name="add_pharmacist_save"),
    path('manage_pharmacist/', manage_pharmacist, name="manage_pharmacist"),
    path('edit_pharmacist/<pharmacist_id>/', edit_pharmacist, name="edit_pharmacist"),
    path('edit_pharmacist_save/', edit_pharmacist_save, name="edit_pharmacist_save"),
    path('delete_pharmacist/<pharmacist_id>/', delete_pharmacist, name="delete_pharmacist"),
    path('add_registration_clerk/', add_registration_clerk, name="add_registration_clerk"),
    path('add_registration_clerk_save/', add_registration_clerk_save, name="add_registration_clerk_save"),
    path('manage_registration_clerk/', manage_registration_clerk, name="manage_registration_clerk"),
    path('edit_registration_clerk/<registration_clerk_id>/', edit_registration_clerk, name="edit_registration_clerk"),
    path('edit_registration_clerk_save/', edit_registration_clerk_save, name="edit_registration_clerk_save"),
    path('delete_registration_clerk/<registration_clerk_id>/', delete_registration_clerk, name="delete_registration_clerk"),
    #path('add_laboratorist/', add_laboratorist, name='add_laboratorist' ),
    #path('add_laboratorist_save', add_laboratorist_save, name='add_laboratorist_save' ),
    
    #doctor urls
    path('doctor_home',doctor_home, name="doctor_home"),
    path('doctor_profile/', doctor_profile, name="doctor_profile"),
    path('submit_doctor_profile/', submit_doctor_profile, name="submit_doctor_profile"),
    path('edit_doctor_profile/', edit_doctor_profile, name="edit_doctor_profile"),
    path('doctor_settings/', doctor_settings, name='doctor_settings'),
    path('doctor_appointments', doctor_appointments, name='doctor_appointments'),
    path('assinged_patient/', assinged_patient, name='assinged_patient'),
    path('discharge_patient/', dicharge_patient, name='dicharge_patient' ),
    path('add_appointment/', add_appointment, name='add_appointment'),
    path('add_appointment_save/', add_appointment_save, name ='add_appointment_save'),
    path('doctor_settings/', settings, name='doctor_settings' ),
    
    #nurse urls
    path('nurse_home', nurse_home, name="nurse_home"),
    path('nurse_profile/', nurse_profile, name="nurse_profile"),
    path('edit_nurse_profile/', edit_nurse_profile, name="edit_nurse_profile"),
    path('submit_nurse_profile/',submit_nurse_profile, name="submit_nurse_profile"),
    # path('doctor_home', doctor_home, name="doctor_home"),

    #Accountant
    path('accountant_home/', accountant_template, name = 'accountant_template' ),

    #Laboratorist
    path('laboratorist_home/', laboratorist_template, name = 'laboratorist_template' ),
    path('lab_home/', lab_home, name='lab_home'),
    path('add_diagnosis_report/', add_diagnosis_report, name='add_diagnosis_report' ),
    path('add_diagnosis/', add_diagnosis, name='add_diagnosis'),
    path('add_diagnosis_report_save/', add_diagnosis_report_save, name = 'add_diagnosis_report_save'),
    path('edit_diagnosis_report/<uuid:id>/', edit_diagnosis_report, name='edit_diagnosis_report' ),
    path('delete_report/<uuid:id>', delete_report, name='delete_report' ),
    path('add_donor/', add_donor, name='add_donor' ),
    path('add_donor_report/', add_donor_report, name='add_donor_report'),
    path('add_donor_report_save/', add_donor_report_save, name='add_donor_report_save'),
    path('edit_donor/<uuid:id>/', edit_donor_report, name='edit_donor' ),
    path('delete_donor/<uuid:id>/', delete_donor, name='delete_donor' ),
    path('blood_bank/', blood_bank, name='blood_bank'),

    #Registration_clerk urls
    path('registration_clerk_home', registration_clerk_home, name="registration_clerk_home"),
    path('registration_clerk_profile/', registration_clerk_profile, name="registration_clerk_profile"),
    path('edit_registration_clerk_profile/',edit_registration_clerk_profile, name="edit_registration_clerk_profile"),
    path('submit_registration_clerk_profile/', submit_registration_clerk_profile, name="submit_registration_clerk_profile"),
    path('edit_registered_patient/<int:registered_patient_id>/', edit_registered_patient, name='edit_registered_patient'),    path('edit_registered_patient_save/', edit_registered_patient_save, name="edit_registered_patient_save"),
    path('delete_registered_patient/<registered_patient_id>/', delete_registered_patient, name="delete_registered_patient"),
    path('book_appointment/<int:registered_patient_id>/', book_appointment, name='book_appointment'),
    path('manage_appointment/', manage_appointment, name='manage_appointment'),
    path('appointment/<int:appointment_id>/edit/', edit_appointment, name='edit_appointment'),
    path('cancel_appointment/<int:appointment_id>/', cancel_appointment, name='cancel_appointment'),

   #pharmacist
    path("pharma/",register_pharmacist,name='pharma'),
    path('dashboard/admin/', admin_dashboard, name='admin'),
    path('product/<int:id>',edit_product,name='edit_product'),
    path('product/create_product',create_product,name='create_product'),
    path('product/delete/<int:id>',delete_product,name='delete_product'),
    path('product/list',product_list,name='product_list'),
    path('dashboard/category/',category,name='category'),
    path('prof/admin/',admin_pharmacy_profile,name='admin_pharmacy_profile'),
    path('prof/admin/create',create_admin_pharmacy_profile,name='create_admin_pharmacy_profile'),
    path('search/',admin_search,name='admin_search'),
    path('search/customer',customer_search,name='customer_search'),   
    path('sales/list',sale_list,name='sale_list'),
    path('sale/list/<int:id>',edit_sale,name='edit_sale'),
    path('sale/create',create_sale,name='create_sale'),
    path('sale/delete/<int:id>/', delete_sale, name='delete_sale'),  
    path('dealer/',dealerlist,name='dealer_list'),
    path('dealer/create',createdealer,name='create_dealer'),
    path('dealer/edit/<int:id>',editdealer,name="edit_dealer"),
    path('dealer/delete/<int:id>',deletedealer,name="delete_dealer"),
    path('dealer/message/<int:id>',dealermessage,name='message_dealer'),
    path('registration_clerk_home', registration_clerk_home, name="registration_clerk_home"),
    path('registration_clerk_profile/', registration_clerk_profile, name="registration_clerk_profile"),
    path('edit_registration_clerk_profile/',edit_registration_clerk_profile, name="edit_registration_clerk_profile"),
    path('submit_registration_clerk_profile/', submit_registration_clerk_profile, name="submit_registration_clerk_profile"),
    path('register_patient/', register_patient, name='register_patient'),
    path('register_patient_save/', register_patient_save, name='register_patient_save'),
    path('manage_registered_patient/', manage_registration_clerk, name="manage_registered_patient"),
    path('registered_patient_list/', registered_patient_list, name='registered_patient_list'),
    path('registered_patient_details/<int:registered_patient_id>/', registered_patient_details, name='registered_patient_details'),
    path('generate_pdf/<int:registered_patient_id>/', generate_pdf, name='generate_pdf'),
    path('forgot-pass',forgotpassword,name="forgot_pswd"),
    path('change-pass/<token>/',changepassword,name="change-pswd"),
    path('add_pharmacist/', add_pharmacist, name="create_pharmacist"),

    path("pharmacist/save/", add_pharmacist_save,name="add_pharmacist_save"),
    path("edit_pharmacist/<int:pharma_id>",edit_pharmacist,name="edit_pharmacist"),
    path('edit_pharmacist_save/',edit_pharmacist_save,name='edit_pharmacist_save'),
    path('delete_pharmacist/<int:pharma_id>',delete_pharmacist,name='delete_pharmacist'),
    path('pharmacist/', pharmacist,name='pharmacist'),
    
    path('prescription/add',create_prescription,name='create_prescription'),
    path('prescription/',managePrescription,name='prescription_list'),
    path('prescription/edit/<int:pk>',editPrescription,name='edit_prescription'),
    path('prescription/delete/<int:pk>',delete_prescription,name='delete_prescription'),
    path('despense/list',dispense_list,name='dispense_list'),
    path('dispense/<int:prescription_id>/', dispense, name='dispense'),
    path('dispense/<int:prescription_id>/<int:dispense_id>/', edit_dispense, name='edit_dispense'),
    path('dispense/<int:prescription_id>/<int:dispense_id>/delete/', delete_dispense, name='delete_dispense'),
    path('profile/pharmacist/',pharmacist_profile,name='pharmacist_profile'),
    path('profile/pharmacist/edit/',edit_pharmacist_profile,name="edit_pharmacist_profile"),
    path('profile/pharmacist/edit/save',submit_pharma_profile,name='submit_pharma_profile'),
    path('patient_profile/',patientProfile,name='patient_profile'),
    path('patient_home/',patientHome,name='patient_home'),
    path('patient_feedback/',patient_feedback,name='patient_feedback'),
    path('staff_feedback_save/', patient_feedback_save, name="patient_feedback_save"),
    path('taken_home/',patient_dispense3,name='taken_home'),
    path('delete_patient_feedback2/<str:pk>/',Patientdeletefeedback, name="delete_fed2"),
    path('delete_dispen/',myPrescriptionDelete,name='taken_delete'),

]
