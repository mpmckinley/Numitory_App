from django.contrib import auth
from django.db.models.aggregates import Count
from django.db.models.expressions import OrderBy
from django.http import response, HttpResponseRedirect,JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User,Group
from django.db import IntegrityError
from django.db.models import Sum
from django.contrib.auth import login, logout, authenticate,update_session_auth_hash
from .forms import ItemCreateForm, TransactionCreateForm, TypeCreateForm, TypeDetlForm, CollectionCreateForm, UserChangeForm, ExtendedUserForm
from .models import Transaction, Type, Collection, Item, UserExtended, MetalPrices
from django.contrib.auth.decorators import login_required
from itertools import chain
import datetime

def home(request):

    if request.user.is_authenticated:
        itemtotal = Item.objects.filter(user=request.user, status='Active').aggregate(Count('id'))
        typetotal = Type.objects.filter(user=request.user).aggregate(Count('id'))
        colltotal = Collection.objects.filter(user=request.user).aggregate(Count('id'))
        items = Item.objects.filter(user=request.user, status='Active')
        transactions = Transaction.objects.filter(user=request.user).order_by('-created')[:5]

        return render(request, 'inventory/home.html', {
            'itemtotal': itemtotal,
            'typetotal': typetotal,
            'colltotal': colltotal,
            'transactions': transactions,
            'page_title': 'Numitory - Home'

            # 'tran_chain': tran_chain,
        })
    else:
        return render(request, 'inventory/home.html')


def get_latest_prices(request):
    prices=MetalPrices.objects.order_by('-updated_at')[:1].values()
    if(not prices):
        prices=[]
    else:
        prices.get()
        # print(prices)
        prices[0]['updated_at']=prices[0]['updated_at'].strftime('%m/%d/%y %H:%M:%S')
    return JsonResponse({'prices':list(prices)})
    
    
# def refresh_latest_pricing(request):
    
    
# ***ATTEMPT AT API CALL
# def navbar(request):
#     import requests
#     import json
    
#     api_request = requests.get('https://www.quandl.com/api/v3/datasets/BTER/BTMETH?start_date=2017-11-08&end_date=2017-11-08&api_key=driYA7Q4oEw7sxoomJVG')
#     api = json.loads(api_request.content)
#     print(api)
#     return render(request, 'inventory/navbar.html', {'api': api})

def about(request):
    return render(request, 'inventory/about.html', {
        'page_title': 'Numitory - About'
    })

def landing(request):
    return render(request, 'inventory/landing.html', {
        'page_title': 'Numitory'
    })

#APPLICATION
@login_required
def inventory(request):
    heading = 'Active'
    items = Item.objects.filter(user=request.user, status='Active')
    types = Type.objects.filter(user=request.user)
    collections = Collection.objects.filter(user=request.user)

    # ***[GIT issue: New User Workflow #17] THIS NEEDS FIXING TO BE LESS CIRCULAR WITH THE VIEW IF NOT--- CREATE A WORKFLOW THAT DISABLES BUTTON AS STARTING Db ENTRIES ARE MADE
    # if items is None or types is None or collections is None:
    #     return redirect('inventory/inventory.html', {
    #     'heading': heading,
    #     'items': items,
    #     'types': types,
    #     'collections': collections,
    # })

    paginator = Paginator(items, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'inventory/inventory.html', {
        'heading': heading,
        'items': items,
        'types': types,
        'collections': collections,
        'page_obj': page_obj,
        'page_title': 'Numitory - My Inventory'

    })

@login_required
def recycle(request):
    heading = 'Recycled'
    items = Item.objects.filter(user=request.user).exclude(status='Active')

    paginator = Paginator(items, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'inventory/inventory.html', {
        'items': items,
        'heading': heading,
        'page_obj': page_obj,
        'page_title': 'Numitory - Recycled Inventory'

    })

@login_required
def itemcreate(request):
    heading = 'Item'
    button = 'Create'
    if request.method == 'GET':
        return render(request, 'inventory/itemcreate.html', {
            'form': ItemCreateForm(user=request.user),
            'heading': heading,
            'button': button,
            'page_title': 'Numitory - Item Create'

        })
    else:
        try:
            form = ItemCreateForm(data=request.POST, files=request.FILES, user=request.user)
            newitem = form.save(commit=False)
            newitem.user = request.user
            newitem.save()
            return redirect('inventory:inventory')
        except ValueError:
            return render(request, 'inventory/itemcreate.html', {
                'form': ItemCreateForm(user=request.user),
                'error': "Field validation error",
            })

@login_required
def itemdetail(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk, user=request.user)
    if request.method == 'GET':
        form = ItemCreateForm(user=request.user, instance=item)
        tranform = TransactionCreateForm(instance=item)
        trans = Transaction.objects.filter(user=request.user, tran_item_id=item_pk).order_by('-id')

        total = Transaction.objects.filter(user=request.user, tran_item_id=item_pk).aggregate(Count('id'))

        # detail = Type.objects.filter(user=request.user, id=item.type_id)
        detail = get_object_or_404(Type, user=request.user, id=item.type_id)

        paginator = Paginator(trans, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'inventory/itemdetail.html', {
            'item': item,
            'form': form,
            'trans': trans,
            'tranform': tranform,
            'total': total,
            'detail': detail,
            'page_obj': page_obj,
            'page_title': 'Numitory - Item Detail'

        })

    if 'item' in request.POST:
        try:
            form = ItemCreateForm(data=request.POST, files=request.FILES, user=request.user, instance=item)
            form.save()
            print (form.data)
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

    # ***TRANSECTION DELETE
    pk = request.POST['pk']
    if request.method == 'POST' and 'delete' in request.POST:
        tran = get_object_or_404(Transaction, pk=pk)
        tran.delete()
        return redirect(request.path_info)

@login_required
def typeinv(request):
    types = Type.objects.filter(user=request.user)
    return render(request, 'inventory/typeinv.html', {
        'types': types,
        'page_title': 'Numitory - My Types'

    })

@login_required
def typecreate(request):
    heading = 'Type'
    button = 'Create'

    if request.method == 'GET':
        return render(request, 'inventory/typecreate.html', {
            'form': TypeCreateForm(),
            'form_detl': TypeDetlForm(),
            'heading': heading,
            'button': button,
            'page_title': 'Numitory - Type Create'

        })
        
    else:
        try:
            form = TypeCreateForm(request.POST)
            form_detl = TypeDetlForm(request.POST)
            newtype = form.save(commit=False)
            newtypedetl = form_detl.save(commit=False)
            newtype.user = request.user
            newtype.save()
            newtypedetl.user = request.user
            newtypedetl.type_id = newtype.id
            newtypedetl.save()
            return redirect('inventory:typeinv')
        except ValueError:
            return render(request, 'inventory/typecreate.html', {
                'form': TypeCreateForm(),
                'form_detl': TypeDetlForm(),
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
            'page_title': 'Numitory - Type Detail'

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
        'page_title': 'Numitory - My Inventory, Types'

    })

@login_required
def collinv(request):
    collections = Collection.objects.filter(user=request.user)

    return render(request, 'inventory/collinv.html', {
        'collections': collections,
        'page_title': 'Numitory - My Collections'

    })

@login_required
def collcreate(request):
    heading = 'Collection'
    button = 'Create'

    if request.method == 'GET':
        return render(request, 'inventory/collcreate.html', {
            'form': CollectionCreateForm(),
            'heading': heading,
            'button': button,
            'page_title': 'Numitory - Collection Create'

        })

    else:
        try:
            form = CollectionCreateForm(request.POST)
            newcoll = form.save(commit=False)
            newcoll.user = request.user
            newcoll.save()
            return redirect('inventory:collinv')
        # except IntegrityError:
        #     return render(request, 'inventory/collectioncreate.html', {'form':CollectionCreateForm(), 'error':"Data duplication error."})
        except ValueError:
            return render(request, 'inventory/collcreate.html', {
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
            'page_title': 'Numitory - Collection Detail'

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
        'page_title': 'Numitory - My Inventory'

    })

#AUTH
def signupuser(request):
    heading = 'Sign Up'
    if request.method == 'GET':
        return render(request, 'inventory/signupuser.html', {
            'form':UserCreationForm(),
            'e_form': ExtendedUserForm(user=''),
            'heading':heading,
            'page_title': 'Numitory - Sign Up'

        })
    else:
        if request.POST['password1'] == request.POST['password2']:
                try:
                    user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                    if(request.POST['user_type'] and request.POST['user_type']!=0):
                        user.save()
                        g=Group.objects.get(id=request.POST['user_type'])
                        g.user_set.add(user)
                        login(request, user)
                        return redirect('/inventory/')
                    else:
                        return render(request, 'inventory/signupuser.html', {
                            'form':UserCreationForm(),
                            'e_form': ExtendedUserForm(''),
                            'heading':heading,
                            'error': "User Type is Required",
                        })
                except IntegrityError:
                    return render(request, 'inventory/signupuser.html', {
                        'form':UserCreationForm(),
                        'e_form': ExtendedUserForm(''),
                        'heading':heading,
                        'error': "Username alerady taken - select another.",
                    })
        else:
            return render(request, 'inventory/signupuser.html', {
                'form':UserCreationForm(),
                'e_form': ExtendedUserForm(''),
                'heading':heading,
                'error': "Passwords did not match.",
            })

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'inventory/loginuser.html', {
            'form': AuthenticationForm(),
            'page_title': 'Numitory - Login'

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
        e_form = ExtendedUserForm(user=user)
        return render(request, 'inventory/edituser.html', {
            'user': user,
            'form':form,
            'e_form':e_form,
            'page_title': 'Numitory - My Profile'

        })
    else:
        try:
            form = UserChangeForm(request.POST, instance=user)
            e_form = ExtendedUserForm(user=user)
            if(form.is_valid()):
                not_empty_data = [ k for k,v in form.cleaned_data.items() if v ]
                form.save(update_fields=not_empty_data)
                if(request.POST['user_type'] and request.POST['user_type']!=0):
                    g=Group.objects.get(id=request.POST['user_type'])
                    query_set = Group.objects.filter(user = user)
                    user.groups.clear()
                    g.user_set.add(user)
                    update_session_auth_hash(request,user_pk)
                    return redirect('inventory:inventory')
                else:
                    return render(request, 'inventory/edituser.html', {
                        'user': user,
                        'form': UserChangeForm(instance=user),
                        'e_form':ExtendedUserForm(user=user),
                        'error':"User Type is Required"
                    })
                # if(e_form.is_valid()):
                    # print(request.POST)
                    # not_empty_data_e = [ k for k,v in e_form.cleaned_data.items() if v ]
                    # e_form.save(update_fields=not_empty_data_e)
                # else:
                    # er_str=""
                    # return render(request, 'inventory/edituser.html', {
                        # 'user': user,
                        # 'form': UserChangeForm(instance=user),
                        # 'e_form':ExtendedUserForm(instance=user.profile),
                        # 'error':e_form.errors.get("__all__")
                    # }) 
            else:
                er_str=""
                return render(request, 'inventory/edituser.html', {
                    'user': user,
                    'form': UserChangeForm(instance=user),
                    'e_form':ExtendedUserForm(user=user),
                    'error':form.errors.get("__all__")
                })  
        except ValueError as e:
            return render(request, 'inventory/edituser.html', {
                'user': user,
                'e_form':ExtendedUserForm(instance=user),
                'form': UserChangeForm(user=user),
                'error':str(e)
            })

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
