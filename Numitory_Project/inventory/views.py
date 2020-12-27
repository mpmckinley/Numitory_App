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
    items = Item.objects.filter(user=request.user, sold=False)
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
            return render(request, 'inventory/itemdetail.html', {'item': item, 'form': ItemCreateForm(), 'error':'You have some bad data in there, try again'})

def typeinv(request):
    types = Type.objects.filter(user=request.user)
    #REMOVED AS UNECSSARY ABOVE ".select_related('type', 'collection')" and ", sold=False"
    return render(request, 'inventory/typeinv.html', {'types': types})

def typecreate(request):
    if request.method == 'GET':
        return render(request, 'inventory/typecreate.html', {'form':TypeCreateForm()})
    else:
        try:
            form = TypeCreateForm(request.POST)
            newtype = form.save(commit=False)
            newtype.user = request.user
            newtype.save()
            return redirect('inventory:typecreate')
        except ValueError:
            return render(request, 'inventory/typecreate.html', {'form':TypeCreateForm(), 'error':"Data validation error"})

def typedetail(request, type_pk):
    type = get_object_or_404(Type, pk=type_pk, user=request.user)
    if request.method == 'GET':
        form = TypeCreateForm(instance=type)
        return render(request, 'inventory/typedetail.html', {'type': type, 'form':form})
    else:
        try:
            form = TypeCreateForm(request.POST, instance=type)
            form.save()
            return redirect('inventory:typeinv')
        except ValueError:
            return render(request, 'inventory/typedetail.html', {'type': type, 'form': TypeCreateForm(), 'error':'You have some bad data in there, try again'})

def typeitems(request, type_pk):
    items = Item.objects.filter(user=request.user, sold=False, type=type_pk)
    #REMOVED AS UNECSSARY ABOVE ".select_related('type', 'collection')"
    return render(request, 'inventory/inventory.html', {'items': items})

def collinv(request):
    collections = Collection.objects.filter(user=request.user)
    #REMOVED AS UNECSSARY ABOVE ".select_related('type', 'collection')" and ", sold=False"
    return render(request, 'inventory/collinv.html', {'collections': collections})

def collcreate(request):
    if request.method == 'GET':
        return render(request, 'inventory/collcreate.html', {'form':CollectionCreateForm()})
    else:
        try:
            form = CollectionCreateForm(request.POST)
            newtype = form.save(commit=False)
            newtype.user = request.user
            newtype.save()
            return redirect('inventory:collinv')
        # except IntegrityError:
        #     return render(request, 'inventory/collectioncreate.html', {'form':CollectionCreateForm(), 'error':"Data duplication error."})
        except ValueError:
            return render(request, 'inventory/collcreate.html', {'form':CollectionCreateForm(), 'error':"Data validation error."})

def colldetail(request, coll_pk):
    collection = get_object_or_404(Collection, pk=coll_pk, user=request.user)
    if request.method == 'GET':
        form = CollectionCreateForm(instance=collection)
        return render(request, 'inventory/colldetail.html', {'collection': collection, 'form':form})
    else:
        try:
            form = CollectionCreateForm(request.POST, instance=collection)
            form.save()
            return redirect('inventory:collinv')
        except ValueError:
            return render(request, 'inventory/colldetail.html', {'collection': collection, 'form': CollectionCreateForm(), 'error':'You have some bad data in there, try again'})

def collitems(request, coll_pk):
    items = Item.objects.filter(user=request.user, sold=False, collection=coll_pk)
    #REMOVED AS UNECSSARY ABOVE ".select_related('type', 'collection')"
    return render(request, 'inventory/inventory.html', {'items': items})

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