from core import models
from django import forms
from django.core.exceptions import ValidationError


class UserCreationForm(forms.ModelForm):


    class Meta:
        model = models.City
        fields = ('name', )


def validate_city(value):
    if not value.isalpha():
        raise ValidationError("City name cannot contain numbers")
    return value



class SearchForm(forms.Form):
    city = forms.CharField(max_length=255,validators=[validate_city])

    
