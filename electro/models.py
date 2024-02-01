from django.db import models
from django.contrib.auth.models import AbstractUser
from decimal import Decimal
from django.utils import timezone



class CustomUser(AbstractUser):
    id = models.AutoField(primary_key=True)
    USER_TYPE_CHOICES = [
        ('user', 'User'),
        ('staff', 'Staff')
        ]
    user_type = models.CharField(max_length=50, choices=USER_TYPE_CHOICES)

    firstname=models.CharField(max_length=255)
    lastname=models.CharField(max_length=255)
    emailid = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True,null=True,blank=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class Invoice(models.Model):
    staff = models.ForeignKey(CustomUser, related_name='generated_invoices', on_delete=models.CASCADE,null=True)
    customer = models.ForeignKey(CustomUser, related_name='invoices', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('paid', 'Paid')], default='pending')
    objects = models.Manager()

class Unit(models.Model):
    staff = models.ForeignKey(CustomUser, related_name='added_units', on_delete=models.CASCADE,null=True)
    user= models.ForeignKey(CustomUser, related_name='received_units', on_delete=models.CASCADE,null=True)
    units=models.IntegerField(default=0)

    amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    due_date = models.DateField(null=True)
    invoice = models.ForeignKey(Invoice, related_name='units', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('paid', 'Paid'), ('overdue', 'Overdue')],
                              default='pending')
    invoiced = models.BooleanField(default=False)
    disconnection_date = models.DateField(null=True, blank=True)
    objects = models.Manager()



class UnitHistory(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # ForeignKey linking to the User model
    units_added = models.IntegerField()
    date_added = models.DateField()
