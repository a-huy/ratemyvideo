from django import forms
from django.conf import settings

import videos.models as videos_models

class RatingCreateForm(forms.ModelForm):
    
    class Meta:
        model = videos_models.Rating

