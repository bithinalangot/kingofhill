from django import forms
from django.db import models 
import re 
SERVICES = (
    ('www','www'),
    ('service', 'service'),
    ('AD', 'AD'),
)

class FlagForm(forms.Form):
    flag = forms.CharField(label="Flag", max_length=32)
    service = forms.CharField(widget=forms.Select(choices=SERVICES))


    def clean_flag(self):
        flag = self.cleaned_data['flag']
        flag_check = re.compile(r"([a-fA-F0-9]{32})")

        if flag_check.match(flag):
            return flag
        else:
            raise forms.ValidationError("Flag should be an md5 value")

    def clean_service(self):
        service_list = ["www","service","AD"]

        service = self.cleaned_data['service']
        if service in service_list:
            return service
        else:
            raise forms.ValidationError("You are trying to enter an invalid service")
        
