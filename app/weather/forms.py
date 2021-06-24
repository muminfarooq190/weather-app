from core import models
from django import forms


class UserCreationForm(forms.ModelForm):


    class Meta:
        model = models.City
        fields = ('name', )
