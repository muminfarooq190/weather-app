from core import models
from django import forms


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Confirmation of password', widget=forms.PasswordInput)

    class Meta:
        model = models.User
        fields = ('email', 'password')

    def clean_password_confirm(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("passwords does not match")
        return password

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        commit=True
        print('*********************************************************')
        if commit:
            user.save()
        return user
