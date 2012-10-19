from django import forms
from django.conf import settings

import accounts.models as accounts_models

class UserCreateForm(forms.ModelForm):
    
    class Meta:
        model = accounts_models.User

class UserUpdateForm(forms.ModelForm):
    
    class Meta:
        model = accounts_models.User

