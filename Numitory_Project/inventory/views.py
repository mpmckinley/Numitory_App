from django.contrib import auth
from django.http import response
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import ItemCreateForm
from .models import Type, Collection, Item

def home(request):
    return render(request, 'inventory/home.html')

def about(request):
    return render(request, 'inventory/about.html')

#APPLICATION
def inventory_home(request):
    return render(request, 'inventory/inventory_home.html')

def itemcreate(request):
    if request.method == 'GET':
        return render(request, 'inventory/itemcreate.html', {'form':ItemCreateForm()})
    else:
        form = ItemCreateForm(request.POST)
        newitem = form.save(commit=False)
        newitem.user = request.user
        # newitem.type_id = request.type_id['type_id']
        # newitem.collection_id = form.get(Collection.id)
        newitem.save()
        return render(request, 'inventory/inventory_home.html')
    
#AUTH
def signupuser(request):
    if request.method == 'GET':
        return render(request, 'inventory/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
                try:
                    user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                    user.save()
                    login(request, user)
                    return redirect(user, '/inventory/')
                except IntegrityError:
                    return render(request, 'inventory/signupuser.html', {'form':UserCreationForm(), 'error':"Username alerady taken - select another."})
        else:
            return render(request, 'inventory/signupuser.html', {'form':UserCreationForm(), 'error':"Passwords did not match."})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'inventory/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'inventory/loginuser.html', {'form':AuthenticationForm(), 'error':"Those aren't good credentials - try again."})
        else:
            login(request, user)
            return redirect('/inventory/')

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')