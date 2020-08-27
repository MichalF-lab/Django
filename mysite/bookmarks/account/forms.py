from django import forms

from django.contrib.auth.models import User

class LoginForm(forms.Form):
    # przygotowanie formy logowania
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    # Widżet genuruje pole HTML

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Hasło',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Powtórz hasło',widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')