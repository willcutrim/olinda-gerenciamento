from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import USerForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


def login_View(request):

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo, {username}!')
                return redirect('home')  # Substitua 'pagina_inicial' pelo nome da sua página inicial
            else:
                messages.error(request, 'Nome de usuário ou senha incorretos.')
        else:
            messages.error(request, 'Nome de usuário ou senha incorretos.')
    else:
        form = AuthenticationForm()
    return render(request, 'html/login.html', {'form': form})


def logout_django(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('login')