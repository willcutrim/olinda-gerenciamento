from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.hashers import check_password




def login_View(request):

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and check_password(password, user.password):
                login(request, user)
                print(request, f'Bem-vindo, {username}!')
                return redirect('home')
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
    


@login_required(login_url="login")
def cadastrar_usuários(request):

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cadastrar-usuarios')
    else:
        form = UserForm()      
        return render(request, 'html/cadastro_de_usuarios.html', {'form': form})
    

@login_required(login_url="login")
def lista_de_usuarios(request):
    items_por_pagina = 10

    users = User.objects.all()

    paginator = Paginator(users, items_por_pagina)

    page = request.GET.get('page')

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'html/lista_de_usuarios.html', {'users': users})


@login_required(login_url="login")
def atualizar_usuario(request, pk):
    user = get_object_or_404(User, id=pk)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        
        if 'username' in form.changed_data:
            new_username = form.cleaned_data['username']
            if User.objects.filter(username=new_username).exclude(id=user.id).exists():
                messages.error(request, 'Um usuário com este nome de usuário já existe.')
                return render(request, 'html/editar_usuario.html', {'form': form, 'user': user})
        
        if form.is_valid():
            form.instance.updated_by = request.user
            form.save()
            messages.success(request, 'Usuário atualizado com sucesso.')
            return redirect('lista-de-usuarios')
    else:
        form = UserForm(instance=user)

    return render(request, 'html/editar_usuario.html', {'form': form, 'user': user})