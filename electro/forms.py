# forms.py
from django import forms
from .models import CustomUser, Unit,Complaint
from django.contrib.auth.forms import AuthenticationForm

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['user_type', 'username', 'first_name', 'last_name', 'email', 'password', 'phone_number']
        widgets = {
            'user_type': forms.Select(attrs={'placeholder': 'Select User Type'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
        }

class FilterCustomersForm(forms.Form):
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES, label='User Type', required=False)
    customer_username = forms.ModelChoiceField(queryset=CustomUser.objects.filter(user_type='user'),
                                               empty_label='Select Customer',
                                               label='Customer Username',
                                               required=False)


class AddUnitsForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['staff','units','due_date','user']

    def __init__(self, *args, **kwargs):
        super(AddUnitsForm, self).__init__(*args, **kwargs)
        # You can customize the queryset as needed, for example, to filter only certain users
        self.fields['staff'].queryset = CustomUser.objects.filter(user_type='staff')
        self.fields['user'].queryset = CustomUser.objects.filter(user_type='user')
class PhoneLoginForm(AuthenticationForm):
    phone_number = forms.CharField(max_length=15)

class InvoiceGenerationForm(forms.Form):
    user = forms.ModelChoiceField(queryset=CustomUser.objects.filter(user_type='user'), label='Select User')
class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name','email','password','phone_number','user_type']
        widgets = {'password': forms.PasswordInput}

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['name', 'email', 'phone', 'message']