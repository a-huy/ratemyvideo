from django import forms

class CSVForm(forms.Form):
    csvfile = forms.FileField(label='Select a file')