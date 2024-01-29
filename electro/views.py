from datetime import timedelta

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.urls import reverse

from .models import CustomUser, Invoice, Unit
from .forms import SignupForm, InvoiceGenerationForm, FilterCustomersForm, AddUnitsForm, PhoneLoginForm
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required


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
                return redirect('/admin/')
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
    for unit in user_units:
        print("this")
        unit.amount = unit.units* 9 # Replace YOUR_PRICE_PER_UNIT with your actual price per unit
        unit.save()

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

def add_units(request):
    staff=request.user

    if request.method == 'POST':
        add_units_form = AddUnitsForm(request.POST)

        if add_units_form.is_valid():
            units = add_units_form.cleaned_data['units']
            due_date = add_units_form.cleaned_data['due_date']
            user=add_units_form.cleaned_data['user']

            # unit_instance = add_units_form.save(commit=False)
            # unit_instance.staff = staff
            # unit_instance.customer = customer
            # unit_instance.save()
            # due_date = add_units_form.cleaned_data['due_date']
            unit_instance, created = Unit.objects.get_or_create(
                user=user,
                staff=staff,
                due_date=due_date,
                defaults={'units': units}
            )
            if not created:
                # Update existing unit
                unit_instance.units += units
                unit_instance.save()
            #
            #
            # # Retrieve the existing unit instance for the specified user and due_date
            # unit_instance = Unit.objects.filter(staff=staff, customer=customer, due_date=due_date).first()
            #
            # if unit_instance:
            #     # Update existing unit
            #     unit_instance.units += units
            #     unit_instance.save()
            # else:
            #     # Create a new unit instance if none exists for the specified date
            #     Unit.objects.create(staff=staff, customer=customer, units=units, due_date=due_date)

            return HttpResponseRedirect(reverse('staff'))
    else:
        # filter_form = FilterCustomersForm()
        add_units_form = AddUnitsForm()

    return render(request, 'electro/add_units.html', {'staff': staff, 'add_units_form': add_units_form})

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


def generate_invoice(request):
    if request.method == 'POST':
        form = InvoiceGenerationForm(request.POST)
        if form.is_valid():
            selected_user = form.cleaned_data['user']
            staff_user = request.user
            units = Unit.objects.filter(user=selected_user)

            # Retrieve pending units for the selected user
            #pending_units = Unit.objects.filter(user=selected_user, staff=staff_user,status='pending', invoiced=False)

            # Create a new invoice for the selected user
            invoice = Invoice.objects.create(customer=selected_user, status='pending')

            # Assign pending units to the invoice
            for unit in units:
                unit.invoice = invoice
                unit.invoiced = True
                unit.save()

            # Update the total amount in the invoice
            total_amount = sum(unit.amount for unit in units)
            invoice.total_amount = total_amount
            invoice.save()
            context = {
                'units': units,
                'total_amount': total_amount,
                # ... other context data ...
            }

            return render(request, 'electro/invoice.html',
                          {'invoice': invoice, 'selected_user': selected_user, 'total_amount': total_amount,'context':context})  # Redirect to the list of invoices
    else:
        form = InvoiceGenerationForm()

    return render(request, 'electro/generate_invoice.html', {'form': form})

def contactus(request):
    return render(request,"electro/contactus.html")
def invoice_list(request):
    return render(request,"electro/invoice.html")
def complaint(request):
    return render(request,"electro/complain.html")


