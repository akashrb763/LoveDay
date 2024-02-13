from django import forms
from lovers.models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('name', 'username', 'age', 'phone_number', 'email', 'password', 'gender')


class LoginForm(forms.Form):
    username_or_phone = forms.CharField(label="Username or Phone Number")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

