from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm

from django.contrib.auth.decorators import login_required

def user_login(request):
    if request.method == 'POST':
    # Jeżeli urzytkownik zarząda metody POST
        form = LoginForm(request.POST)
        # Pobierz dane
        if form.is_valid():
        # Czy dane spełniają normy
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            # Negocjacja z bazą danych czy dane są poprawne
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # Rozpoczyna sesje użytkownika
                    return HttpResponse('Uwierzytelnienie zakończyło się sukcesem.')
                else:
                    return HttpResponse('Konto jest zablokowane.')
            else:
                return HttpResponse('Nieprawidłowe dane uwierzytelniające.')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

@login_required
# Jeżeli użytkownik poprawnie się zalogował
# Strona do której próbował uzyskać dostęp zostanie zapisana w zminnnej next
def dashboard(request):
    return render(request,'account/dashboard.html',{'section': 'dashboard'})
    # dasboard panel głowny

def register(request):
    if request.method == 'POST':
            user_form = UserRegistrationForm(request.POST)
            if user_form.is_valid():
                new_user = user_form.save(commit=False)
                # Utworzenie nowego obiektu użytkownika, ale jeszcze nie zapisujemy go w bazie danych.
                new_user.set_password(user_form.cleaned_data['password'])
                # Ustawienie wybranego hasła.
                new_user.save()
                # Zapisanie obiektu User.
            return render(request,'account/register_done.html',{'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,'account/register.html',{'user_form': user_form})