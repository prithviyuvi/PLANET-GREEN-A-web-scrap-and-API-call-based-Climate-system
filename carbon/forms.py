from django.contrib.auth.models import User, auth
from django import forms

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','username','email']