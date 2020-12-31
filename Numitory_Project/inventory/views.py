from django.contrib import auth
from django.db.models.aggregates import Count
from django.db.models.expressions import OrderBy
from django.http import response, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Sum
from django.contrib.auth import login, logout, authenticate,update_session_auth_hash
from .forms import ItemCreateForm, TransactionCreateForm, TypeCreateForm, CollectionCreateForm, UserChangeForm
from .models import Transaction, Type, Collection, Item
from django.contrib.auth.decorators import login_required


def home(request):
    if request.user.is_authenticated:
        itemtotal = Item.objects.filter(user=request.user, status='Active').aggregate(Count('id'))
        typetotal = Type.objects.filter(user=request.user).aggregate(Count('id'))
        colltotal = Collection.objects.filter(user=request.user).aggregate(Count('id'))

        return render(request, 'inventory/home.html', {
            'itemtotal': itemtotal,
            'typetotal': typetotal,
            'colltotal': colltotal,
        })
    else:
        return render(request, 'inventory/home.html')


def about(request):
    return render(request, 'inventory/about.html')

#APPLICATION
@login_required
def inventory(request):
    heading = 'Active'
    items = Item.objects.filter(user=request.user, status='Active')

    paginator = Paginator(items, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'inventory/inventory.html', {
        'items': items,
        'heading': heading,
        'page_obj': page_obj,
    })

@login_required
def recycle(request):
    heading = 'Recycled'
    items = Item.objects.filter(user=request.user).exclude(status='Active')

    paginator = Paginator(items, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    #REMOVED AS UNECSSARY ABOVE ".select_related('type', 'collection')"
    return render(request, 'inventory/inventory.html', {
        'items': items,
        'heading': heading,
        'page_obj': page_obj,
    })

@login_required
def itemcreate(request):
    heading = 'Item'
    button = 'Create'
    if request.method == 'GET':
        return render(request, 'inventory/create.html', {
            'form': ItemCreateForm(user=request.user),
            'heading': heading,
            'button': button,
        })
    else:
        try:
            form = ItemCreateForm(data=request.POST, user=request.user)
            newitem = form.save(commit=False)
            newitem.user = request.user
            newitem.save()
            return redirect('inventory:inventory')
        except ValueError:
            return render(request, 'inventory/create.html', {
                'form': ItemCreateForm(user=request.user),
                'error': "Field validation error",
            })

@login_required
def itemdetail(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk, user=request.user)
    if request.method == 'GET':
        form = ItemCreateForm(user=request.user, instance=item)
        trans = Transaction.objects.filter(user=request.user, tran_item_id=item_pk).order_by('-id')
        tranform = TransactionCreateForm(instance=item)

        total = Transaction.objects.filter(user=request.user, tran_item_id=item_pk).aggregate(Sum('tran_quantity'))

        paginator = Paginator(trans, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'inventory/itemdetail.html', {
            'item': item,
            'form': form,
            'tranform': tranform,
            'trans': trans,
            'total': total,
            'page_obj': page_obj,
        })
    if 'item' in request.POST:
        try:
            form = ItemCreateForm(data=request.POST, user=request.user, instance=item)
            form.save()
            return redirect('inventory:inventory')
        except ValueError:
            return render(request, 'inventory/itemdetail.html', {
                'item': item,
                'form': ItemCreateForm(user=request.user, instance=item),
                'tranform': TransactionCreateForm(),
                'error':'You have some bad data in there, try again',
            })
    if 'tran' in request.POST:
        try:
            tranform = TransactionCreateForm(data=request.POST)
            newtran = tranform.save(commit=False)
            newtran.user = request.user
            newtran.tran_item_id = item_pk
            newtran.save()
            return redirect(request.path_info)
        except ValueError:
            return render(request, 'inventory/itemdetail.html', {
                'item': item,
                'form': ItemCreateForm(user=request.user, instance=item),
                'tranform': TransactionCreateForm(),
                'error':'You had some bad data in your tran form, try again',
            })
    # ***NEED TO WORK ON THIS
    pk = request.POST['pk']
    if request.method == 'POST' and 'delete' in request.POST:
        tran = get_object_or_404(Transaction, pk=pk)
        tran.delete()
        return redirect(request.path_info)

@login_required
def typeinv(request):
    types = Type.objects.filter(user=request.user)
    #REMOVED AS UNECSSARY ABOVE ".select_related('type', 'collection')" and ", status='A'"
    return render(request, 'inventory/typeinv.html', {
        'types': types,
    })

@login_required
def typecreate(request):
    heading = 'Type'
    button = 'Create'
    if request.method == 'GET':
        return render(request, 'inventory/create.html', {
            'form': TypeCreateForm(),
            'heading': heading,
            'button': button,
        })
    else:
        try:
            form = TypeCreateForm(request.POST)
            newtype = form.save(commit=False)
            newtype.user = request.user
            newtype.save()
            return redirect('inventory:typeinv')
        except ValueError:
            return render(request, 'inventory/create.html', {
                'form': TypeCreateForm(),
                'error': "Data validation error",
            })

@login_required
def typedetail(request, type_pk):
    type = get_object_or_404(Type, pk=type_pk, user=request.user)
    if request.method == 'GET':
        form = TypeCreateForm(instance=type)
        return render(request, 'inventory/typedetail.html', {
            'type': type,
            'form': form,
        })
    else:
        try:
            form = TypeCreateForm(request.POST, instance=type)
            form.save()
            return redirect('inventory:typeinv')
        except ValueError:
            return render(request, 'inventory/typedetail.html', {
                'type': type,
                'form': TypeCreateForm(),
                'error':'You have some bad data in there, try again',
            })

@login_required
def typeitems(request, type_pk):
    heading = Type.objects.values_list('type_name', flat=True).get(id=type_pk)
    items = Item.objects.filter(user=request.user, status='Active', type=type_pk)

    paginator = Paginator(items, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'inventory/inventory.html', {
        'items': items,
        'heading': heading,
        'page_obj': page_obj,
    })

@login_required
def collinv(request):
    collections = Collection.objects.filter(user=request.user)
    #REMOVED AS UNECSSARY ABOVE ".select_related('type', 'collection')" and ", status='A'"
    return render(request, 'inventory/collinv.html', {
        'collections': collections,
    })

@login_required
def collcreate(request):
    heading = 'Collection'
    button = 'Create'
    if request.method == 'GET':
        return render(request, 'inventory/create.html', {
            'form': CollectionCreateForm(),
            'heading': heading,
            'button': button,
        })
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
            return render(request, 'inventory/create.html', {
                'form': CollectionCreateForm(),
                'error': "Data validation error.",
            })

@login_required
def colldetail(request, coll_pk):
    collection = get_object_or_404(Collection, pk=coll_pk, user=request.user)
    if request.method == 'GET':
        form = CollectionCreateForm(instance=collection)
        return render(request, 'inventory/colldetail.html', {
            'collection': collection,
            'form': form,
        })
    else:
        try:
            form = CollectionCreateForm(request.POST, instance=collection)
            form.save()
            return redirect('inventory:collinv')
        except ValueError:
            return render(request, 'inventory/colldetail.html', {
                'collection': collection,
                'form': CollectionCreateForm(),
                 'error':'You have some bad data in there, try again',
                })

@login_required
def collitems(request, coll_pk):
    heading = Collection.objects.values_list('coll_name', flat=True).get(id=coll_pk)
    items = Item.objects.filter(user=request.user, status='Active', collection=coll_pk)

    paginator = Paginator(items, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'inventory/inventory.html', {
        'items': items,
        'heading': heading,
        'page_obj': page_obj,
    })

#AUTH
def signupuser(request):
    heading = 'Sign Up'
    if request.method == 'GET':
        return render(request, 'inventory/signupuser.html', {
            'form': UserCreationForm(),
            'heading':heading,
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
                try:
                    user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                    user.save()
                    login(request, user)
                    return redirect('/inventory/')
                except IntegrityError:
                    return render(request, 'inventory/signupuser.html', {
                        'form': UserCreationForm(),
                        'error': "Username alerady taken - select another.",
                    })
        else:
            return render(request, 'inventory/signupuser.html', {
                'form': UserCreationForm(),
                'error': "Passwords did not match.",
            })

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'inventory/loginuser.html', {
            'form': AuthenticationForm(),
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'inventory/loginuser.html', {
                'form': AuthenticationForm(),
                'error': "Those aren't good credentials - try again.",
            })
        else:
            login(request, user)
            return redirect('/inventory/')

def edituser(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    if request.method == 'GET':
        form = UserChangeForm(instance=user)
        return render(request, 'inventory/edituser.html', {
            'user': user,
            'form':form,
        })
    else:
        try:
            form = UserChangeForm(request.POST, instance=user)
            if(form.is_valid()):
                form.save()
                update_session_auth_hash(request,user)
                return redirect('inventory:inventory')
            else:
                er_str=""
                return render(request, 'inventory/edituser.html', {
                    'user': user,
                    'form': UserChangeForm(instance=user),
                    'error':form.errors.get("__all__")
                })  
        except ValueError as e:
            return render(request, 'inventory/edituser.html', {
                'user': user,
                'form': UserChangeForm(instance=user),
                'error':str(e)
            })

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
