from django.urls import path
from .import views
urlpatterns = [
    path('',views.home,name='homepage'),
    path('user/',views.user,name='user'),
    path('signup/',views.signup,name='signup'),
    path('userhomepage/',views.user_homepage,name='userhomepage'),
    path('add_units/',views.add_units,name='add_units'),
    path('staff/',views.staff,name='staff'),
    path('aboutus/',views.aboutus,name='aboutus'),
    path('bill_login',views.billinglogin,name='bill_login'),
    path('billinfo/',views.billinfo,name='billinfo'),

    path('billcalculator/',views.billcalculator,name="calc"),
    path('paybill/',views.paybill,name='paybill'),
    path('generateinvoice/',views.generate_invoice,name='generate_invoice'),
    path('contactus/',views.contactus,name='contactus'),
    path('invoicelist/',views.invoice_list,name='invoice_list'),
    path('complaint.',views.complaint,name='complaint')
]

