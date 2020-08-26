from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm

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
# Jeżeli nie parametr next przekieruje go strony logowania
def dashboard(request):
    return render(request,'account/dashboard.html',{'section': 'dashboard'})
    # dasboard panel głowny