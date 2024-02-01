from datetime import timedelta
from django.http import HttpResponse

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.views import View

from .models import CustomUser, Invoice, Unit, UnitHistory
from .forms import SignupForm, InvoiceGenerationForm, FilterCustomersForm, AddUnitsForm, PhoneLoginForm
from django.contrib import messages
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from chartjs.views.lines import BaseLineChartView
from django.utils import timezone
from django.db import transaction
from django.contrib.auth.decorators import login_required


def my_admin(request):
    return render(request,"electro/admin.html")
def home(request):
    return render(request, "electro/index.html")


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.user_type = form.cleaned_data['user_type']
            user.save()

            username = user.username
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # email_id = user.email
            password = form.cleaned_data['password']
            # phone_number = form.cleaned_data['phone_number']
            # users = User.objects.create_user(username=username, email=email_id, password=password)
            return redirect('user')

    else:
        form = SignupForm()

    return render(request, "electro/signup.html", {'form': form})


def user(request):
    if request.method == "POST":
        customerid = request.POST["cust_id"]
        password = request.POST["pass"]
        user = authenticate(request, username=customerid, password=password)

        if user is not None:
            login(request, user)

            # Access user_type from the associated CustomUser model
            user_type = request.user.user_type
            print(user_type)

            if user.is_superuser:
                print("reached staff")
                return redirect('myadmin')
            elif user.is_staff or user_type == 'staff':
                print("Staff")
                return redirect('staff')
            else:
                return redirect('userhomepage')

    return render(request, "electro/user.html")


def staff(request):
    regular_users = CustomUser.objects.filter(user_type='user')
    return render(request, "electro/staffhomepage.html", {'regular_users': regular_users})


def user_homepage(request):
    if request.user.is_authenticated:
        print("Authenticated User:", request.user.id)
    # user_units = Unit.objects.filter(customer=request.user)
    user_units = Unit.objects.filter(user_id=request.user.id)
    print(user_units)
    user_info = {
        'username': request.user.username,
        'first_name': request.user.first_name,
    }
    print(user_info)






    return render(request, "electro/userhomepage.html", {'user_info': user_info, 'user_units': user_units})


def aboutus(request):
    return render(request, "electro/aboutus.html")


def billinglogin(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        user = authenticate(request, phone_number=phone_number)

        if user is not None:
            print("User authenticated successfully")
            messages.success(request, 'Successfully logged in.')
            login(request, user)
            return redirect('billinfo')
        else:
            print("Authentication failed")
            messages.error(request, 'Invalid phone number.')

    else:
        form = PhoneLoginForm()

        return render(request, 'electro/billinglogin.html', {'form': form})


def billinfo(request):
    user = request.user
    unit_instance = Unit.objects.filter(user=user).latest('due_date')


    # Get additional user information
    user_name = f"{user.first_name} {user.last_name}"
    phone_number = user.phone_number
    due_date = unit_instance.due_date
    amount= unit_instance.amount
    disconnection_due_date = due_date + timedelta(days=7)

    context = {
        'user_name': user_name,
        'phone_number': phone_number,
        'due_date': due_date,
        'disconnection_due_date': disconnection_due_date,
        'amount':amount
    }

    return render(request, "electro/billdetails.html", context)

def download_receipt(request):
    # Retrieve data needed for the receipt
    user = request.user
    unit_instance = Unit.objects.filter(user=user).latest('due_date')

    # Get additional user information
    user_name = f"{user.first_name} {user.last_name}"
    phone_number = user.phone_number
    due_date = unit_instance.due_date
    amount = unit_instance.amount
    disconnection_due_date = due_date + timedelta(days=7)

    context = {
        'user_name': user_name,
        'phone_number': phone_number,
        'due_date': due_date,
        'disconnection_due_date': disconnection_due_date,
        'amount': amount
    }

    # Render the receipt as HTML
    receipt_content = render_to_string("electro/download_invoice.html", context)

    # Create a response with the receipt content and appropriate headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="receipt.pdf"'

    # Create a PDF from the HTML content using xhtml2pdf
    pisa_status = pisa.CreatePDF(receipt_content, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + receipt_content + '</pre>')
    return response



def add_units(request):
    staff = request.user

    if request.method == 'POST':
        add_units_form = AddUnitsForm(request.POST)

        if add_units_form.is_valid():
            units = add_units_form.cleaned_data['units']
            due_date = add_units_form.cleaned_data['due_date']
            user = add_units_form.cleaned_data['user']
            existing_unit = Unit.objects.filter(user=user).first()
            if existing_unit:
                amount=(units-existing_unit.units)*9
                # Move existing units to history
                UnitHistory.objects.create(
                    user=existing_unit.user,
                    units_added=existing_unit.units,
                    amount=existing_unit.amount,
                    date_added=existing_unit.due_date
                )
                existing_unit.units = units
                existing_unit.amount = amount
                existing_unit.due_date = due_date
                existing_unit.save()
            else:
                # Create a new unit record
                Unit.objects.create(user=user, units=units, due_date=due_date,amount=units*9)


            # Get the existing unit record for the user and due date

            return HttpResponseRedirect(reverse('staff'))
    else:
        add_units_form = AddUnitsForm()

    return render(request, 'electro/add_units.html', {'add_units_form': add_units_form})

def billcalculator(request):
    user = request.user
    try:
        unit_instance = Unit.objects.get(user=user)
        user_units = unit_instance.units
    except Unit.DoesNotExist:
        user_units = 0
    context = {
    'user_phone_number': user.phone_number,
    'user_units': user_units,
        }
    return render(request,"electro/billcalculator.html",context)
def paybill(request):
    return render(request,"electro/paybill.html")



def contactus(request):
    return render(request,"electro/contactus.html")
def invoice_list(request):
    user = request.user
    user_name = f"{user.first_name} {user.last_name}"
    phone_number = user.phone_number
    email=user.email

    units= Unit.objects.get(user=user)
    invoice = Invoice.objects.create(customer=user, status='pending')
    units_to_update = Unit.objects.filter(user=user, status='pending', invoiced=False)
    units_to_update.update(status='paid', invoice=invoice, invoiced=True)
    invoice = Invoice.objects.create(customer=user, status='paid')
    amount = units.amount
    unit=units.units
    context = {
        'user_name': user_name,
        'phone_number': phone_number,
        'email': email,
        'amount':amount,
        'unit':unit
    }

    return render(request,"electro/invoice.html",context)
def download_invoice(request):
    user = request.user
    user_name = f"{user.first_name} {user.last_name}"
    phone_number = user.phone_number
    email = user.email

    units = Unit.objects.get(user=user)
    invoice = Invoice.objects.create(customer=user, status='pending')
    units_to_update = Unit.objects.filter(user=user, status='pending', invoiced=False)
    units_to_update.update(status='paid', invoice=invoice, invoiced=True)
    invoice = Invoice.objects.create(customer=user, status='paid')
    amount = units.amount
    unit = units.units
    context = {
        'user_name': user_name,
        'phone_number': phone_number,
        'email': email,
        'amount': amount,
        'unit': unit
    }
    invoice_content = render_to_string("electro/download_invoice.html", context)

    # Create a response with the receipt content and appropriate headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    # Create a PDF from the HTML content using xhtml2pdf
    pisa_status = pisa.CreatePDF(invoice_content, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + invoice_content + '</pre>')
    return response


def complaint(request):
    return render(request,"electro/complain.html")


def user_history(request):
    # Retrieve the logged-in user's history
    user_history= UnitHistory.objects.filter(user=request.user)

    return render(request, 'electro/user_history.html', {'user_history': user_history})


class UserDashboardView(View):
    template_name = 'electro/user_dashboard.html'

    def get(self, request, *args, **kwargs):
        # Retrieve data from the database
        units_data = UnitHistory.objects.filter(user=request.user)

        # Extract labels, units, and amounts from the queryset
        labels = [data.date_added.strftime('%Y-%m-%d') for data in units_data]
        units = [float(data.units_added) for data in units_data]
        amounts = [float(data.amount) for data in units_data]

        # Pass data to the template
        context = {
            'labels': labels,
            'units': units,
            'amounts': amounts,
        }
        return render(request, self.template_name, context)
def manageuser(request):
    regular_users = CustomUser.objects.filter(is_superuser=False)
    return render(request,"electro/manageuser.html",{'regular_users': regular_users})


