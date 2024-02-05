from django.urls import path
from .import views
urlpatterns = [
    path('',views.home,name='homepage'),
    path('myadmin/',views.my_admin,name='myadmin'),
    path('adduser/',views.admin_adduser,name='adduser'),
    path('user/',views.user,name='user'),
    path('signup/',views.signup,name='signup'),
    path('userhomepage/',views.user_homepage,name='userhomepage'),
    path('add_units/',views.add_units,name='add_units'),
    path('staff/',views.staff,name='staff'),
    path('aboutus/',views.aboutus,name='aboutus'),
    path('bill_login',views.billinglogin,name='bill_login'),
    path('billinfo/',views.billinfo,name='billinfo'),
    path('download_receipt/',views.download_receipt, name='download_receipt'),
    path('user_history/', views.user_history, name='user_history'),
    path('billcalculator/',views.billcalculator,name="calc"),

    path('paybill/',views.paybill,name='paybill'),
    #path('generateinvoice/',views.generate_invoice,name='generate_invoice'),
    path('contactus/',views.contactus,name='contactus'),
    path('invoicelist/',views.invoice_list,name='invoice_list'),
    path('downloadinvoice/',views.download_invoice,name='download_invoice'),
    path('dashboard/', views.UserDashboardView.as_view(), name='user_dashboard'),
    path('manageuser/',views.manageuser,name='manage'),
    path('admindashboard/',views.admin_dashboard,name='admindashboard'),
    path('staffdashboard/',views.staffdashboard,name='staffdashboard'),
    path('complain/', views.complain_form, name='complain_form'),
    path('complaints/', views.view_complaints, name='complaints'),
]

