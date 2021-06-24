from core import models
from django import forms


class UserCreationForm(forms.ModelForm):


    class Meta:
        model = models.City
        fields = ('name', )



    def save(self, commit=True):
        # Save the provided password in hashed format
        city = super().save(commit=False)
        commit=True
        print('*********************************************************')
        if commit:
            city.save()
        return city
