from django import forms

class LoginForm(forms.Form):
    # przygotowanie formy logowania
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    # Widżet genuruje pole HTML