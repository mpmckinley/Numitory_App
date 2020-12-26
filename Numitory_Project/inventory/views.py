from django.contrib import auth
from django.http import response
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import ItemCreateForm, TypeCreateForm, CollectionCreateForm
from .models import Type, Collection, Item

def home(request):
    return render(request, 'inventory/home.html')

def about(request):
    return render(request, 'inventory/about.html')

#APPLICATION
def inventory(request):
    items = Item.objects.filter(user=request.user, recycled=False)
    #REMOVED AS UNECSSARY ABOVE ".select_related('type', 'collection')"
    return render(request, 'inventory/inventory.html', {'items': items})

def itemcreate(request):
    if request.method == 'GET':
        return render(request, 'inventory/itemcreate.html', {'form':ItemCreateForm()})
    else:
        try:
            form = ItemCreateForm(request.POST)
            newitem = form.save(commit=False)
            newitem.user = request.user
            newitem.save()
            return redirect('inventory:inventory')
        except ValueError:
            return render(request, 'inventory/itemcreate.html', {'form':ItemCreateForm(), 'error':"Field validation error"})

def itemdetail(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk, user=request.user)
    if request.method == 'GET':
        form = ItemCreateForm(instance=item)
        return render(request, 'inventory/itemdetail.html', {'item': item, 'form':form})
    else:
        try:
            form = ItemCreateForm(request.POST, instance=item)
            form.save()
            return redirect('inventory:inventory')
        except ValueError:
            return render(request, 'inventory/itemdetail.html', {'item': item, 'error':'You have some bad data in there, try again'})
            
def typecreate(request):
    if request.method == 'GET':
        return render(request, 'inventory/typecreate.html', {'form':TypeCreateForm()})
    else:
        try:
            form = TypeCreateForm(request.POST)
            newtype = form.save(commit=False)
            newtype.user = request.user
            newtype.save()
            return redirect('inventory:inventory')
        except ValueError:
            return render(request, 'inventory/typecreate.html', {'form':TypeCreateForm(), 'error':"Data validation error"})

def collectioncreate(request):
    if request.method == 'GET':
        return render(request, 'inventory/collectioncreate.html', {'form':CollectionCreateForm()})
    else:
        try:
            form = CollectionCreateForm(request.POST)
            newtype = form.save(commit=False)
            newtype.user = request.user
            newtype.save()
            return redirect('inventory:inventory')
        # except IntegrityError:
        #     return render(request, 'inventory/collectioncreate.html', {'form':CollectionCreateForm(), 'error':"Data duplication error."})
        except ValueError:
            return render(request, 'inventory/collectioncreate.html', {'form':CollectionCreateForm(), 'error':"Data validation error."})

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