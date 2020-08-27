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

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Hasła nie są identyczne.')
        return cd['password2']