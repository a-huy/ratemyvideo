from django import forms
from django.conf import settings

import accounts.models as accounts_models

class UserCreateForm(forms.ModelForm):

    earned = forms.DecimalField(required=False)
    rated = forms.IntegerField(required=False)
    liked = forms.IntegerField(required=False)
    commented = forms.IntegerField(required=False)
    age = forms.IntegerField(required=False)
    karma = forms.IntegerField(required=False)
    subscribed = forms.IntegerField(required=False)

    class Meta:
        model = accounts_models.User

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = accounts_models.User

class InviteCreateForm(forms.ModelForm):

    class Meta:
        model = accounts_models.InviteRequest
