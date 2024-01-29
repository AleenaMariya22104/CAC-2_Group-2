# your_app/backend.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class PhoneBackend(ModelBackend):
    def authenticate(self, request,phone_number=None,**kwargs):
        User = get_user_model()

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return None

        return user

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
