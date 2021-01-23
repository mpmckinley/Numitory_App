from django.contrib import auth
from django.db.models.aggregates import Count
from django.db.models.expressions import OrderBy
from django.http import response, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User,Group
from django.db import IntegrityError
from django.db.models import Sum
from django.contrib.auth import login, logout, authenticate,update_session_auth_hash
from .forms import (ItemCreateForm,
                    QuickAddForm,
                    TransactionCreateForm,
                    TypeCreateForm,
                    CollectionCreateForm,
                    UserChangeForm,
                    ExtendedUserForm,
                    ExportForm,
                    ExportFilterForm,
)
from .models import Transaction, Type, Collection, Item, UserExtended, MetalPrices
from django.contrib.auth.decorators import login_required
from itertools import chain
from decouple import config
import datetime
import requests
import json
from newsapi import NewsApiClient
import datetime
import csv

def home(request):

    if request.user.is_authenticated:
        itemtotal = Item.objects.filter(user=request.user, status='Active').aggregate(Count('id'))
        typetotal = Type.objects.filter(user=request.user).aggregate(Count('id'))
        colltotal = Collection.objects.filter(user=request.user).aggregate(Count('id'))
        items = Item.objects.filter(user=request.user, status='Active').order_by('-created')[:10]
        transactions = Transaction.objects.filter(user=request.user).order_by('-created')[:5]
        images = Item.objects.filter(user=request.user, status='Active').exclude(item_image='')[:6]
        prices=MetalPrices.objects.order_by('-updated_at')[:1].values()

        metalprices=MetalPrices.objects.order_by('-updated_at')[:1].values()
        if(not metalprices):
            metalprices=[]
        else:
            metalprices.get()
            metalprices[0]['gold_price']="{:.2f}".format(metalprices[0]['gold_price'])
            metalprices[0]['silver_price']="{:.2f}".format(metalprices[0]['silver_price'])
            metalprices[0]['platinum_price']="{:.2f}".format(metalprices[0]['platinum_price'])
            metalprices[0]['palladium_price']="{:.2f}".format(metalprices[0]['palladium_price'])
            metalprices[0]['updated_at']=metalprices[0]['updated_at'].strftime('%m/%d/%y %H:%M:%S')
        
        news_key = config("API_KEY")
        newsapi = NewsApiClient(api_key=news_key)
        
        top_headlines = newsapi.get_everything(q='silver OR gold OR platinum OR palladium OR numismatic OR coin OR coins OR PCGS OR NGC OR ANACS OR bullion AND precious NOT witcher NOT movies NOT Rs',
            language='en',
            sort_by='publishedAt',
            page=1,
        )

        if request.method == 'POST':
            try:
                form = QuickAddForm(data=request.POST, files=request.FILES, user=request.user)
                newitem = form.save(commit=False)
                newitem.user = request.user
                newitem.save()
                return redirect('home')
            except ValueError:
                return render(request, 'home', {
                    'form': QuickAddForm(user=request.user),
                    'error': "Field validation error",
                })

        return render(request, 'inventory/home.html', {
            'itemtotal': itemtotal,
            'typetotal': typetotal,
            'colltotal': colltotal,
            'metalprices':metalprices[0],
            'items': items,
            'transactions': transactions,
            'page_title': 'Numitory - Home',
            'top_headlines': top_headlines,
            'images': images,
            'prices': prices,
            'form': QuickAddForm(user=request.user),
            'button': 'Create',
        })
    else:
        return render(request, 'inventory/home.html')


def get_latest_prices(request):
    prices=MetalPrices.objects.order_by('-updated_at')[:1].values()
    if(not prices):
        prices=[]
    else:
        prices.get()
        prices[0]['gold_price']="{:.2f}".format(prices[0]['gold_price'])
        prices[0]['silver_price']="{:.2f}".format(prices[0]['silver_price'])
        prices[0]['platinum_price']="{:.2f}".format(prices[0]['platinum_price'])
        prices[0]['palladium_price']="{:.2f}".format(prices[0]['palladium_price'])
        prices[0]['updated_at']=prices[0]['updated_at'].strftime('%m/%d/%y')
    return JsonResponse({'prices':list(prices)})

def silverChart(request):
    labels = []
    data = []

    queryset = MetalPrices.objects.values('updated_at', 'silver_price').order_by('updated_at')
    for entry in queryset:
        labels.append(entry['updated_at'])
        data.append(entry['silver_price'])
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

def goldChart(request):
    labels = []
    data = []

    queryset = MetalPrices.objects.values('updated_at', 'gold_price').order_by('updated_at')
    for entry in queryset:
        labels.append(entry['updated_at'])
        data.append(entry['gold_price'])
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })
    
def refresh_latest_pricing(request):
    api_key=config('METAL_PRICES_API_KEY')
    api_request = requests.get('https://metals-api.com/api/latest?access_key='+api_key+'&base=USD&symbols=XAU%2CXAG%2CXPD%2CXPT%2CXRH')
    api = json.loads(api_request.content)
    base_curr=api['base']
    rates=api['rates']
    base_price=rates[base_curr]
    gold_price=base_price/rates['XAU']
    silver_price=base_price/rates['XAG']
    platinum_price=base_price/rates['XPT']
    palladium_price=base_price/rates['XPD']
    prices=MetalPrices(gold_price=gold_price,silver_price=silver_price,platinum_price=platinum_price,palladium_price=palladium_price)
    prices.save()
    return render(request, 'inventory/navbar.html', {'api': rates})
    

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

    return render(request, 'inventory/inventory.html', {
        'heading': heading,
        'items': items,
        'types': types,
        'collections': collections,
        'page_title': 'Numitory - My Inventory',
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
        'page_title': 'Numitory - My Types',
    })

@login_required
def typecreate(request):
    heading = 'Type'
    button = 'Create'

    if request.method == 'GET':
        return render(request, 'inventory/typecreate.html', {
            'form': TypeCreateForm(),
            # 'form_detl': TypeDetlForm(),
            'heading': heading,
            'button': button,
            'page_title': 'Numitory - Type Create'

        })
        
    else:
        try:
            form = TypeCreateForm(request.POST)
            # form_detl = TypeDetlForm(request.POST)
            newtype = form.save(commit=False)
            # newtypedetl = form_detl.save(commit=False)
            newtype.user = request.user
            newtype.save()
            # newtypedetl.user = request.user
            # newtypedetl.type_id = newtype.id
            # newtypedetl.save()
            return redirect('inventory:typeinv')
        except ValueError:
            return render(request, 'inventory/typecreate.html', {
                'form': TypeCreateForm(),
                # 'form_detl': TypeDetlForm(),
                'error': "Data validation error",
            })

@login_required
def typedetail(request, type_pk):
    type = get_object_or_404(Type, pk=type_pk, user=request.user)
    heading = Type.objects.values_list('longname', flat=True).get(id=type_pk)

    if request.method == 'GET':
        form = TypeCreateForm(instance=type)
        return render(request, 'inventory/typedetail.html', {
            'type': type,
            'form': form,
            'page_title': 'Numitory - Type Detail',
            'heading': heading,
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
    heading = Type.objects.values_list('longname', flat=True).get(id=type_pk)
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
        if request.user.is_authenticated:
            return redirect('/inventory/')
        else:
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
            return redirect('home')

def edituser(request):
    if('_auth_user_id' in request.session):
        user = get_object_or_404(User, pk=request.session['_auth_user_id'])
    else:
        return redirect('/login/')
        
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
                    update_session_auth_hash(request,request.session['_auth_user_id'])
                    return redirect('inventory:inventory')
                else:
                    return render(request, 'inventory/edituser.html', {
                        'user': user,
                        'form': UserChangeForm(instance=user),
                        'e_form':ExtendedUserForm(user=user),
                        'error':"User Type is Required"
                    })
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

@login_required
def export(request):
    user = request.user
    user_obj = User.objects.get(id=request.user.id) #used for our form.
    
    #Request for exporting is via POST. 
    
    if request.method == 'POST':
        #Due to the query which happens in ExportForm()
        #We need to input the current user. 
        form = ExportForm(request.POST,name=user_obj)
        form_filter = ExportFilterForm(request.POST,name=user_obj)
        #If form fails, return user to the form and show errors. 
        if not form.is_valid() or not form_filter.is_valid(): 
            
            content = {  
                    'form' : form,
                    'form_f' : form_filter,
                  }
            return render(request, 'inventory/export.html', content)
        
        #Filter the collections
        collections = form.cleaned_data['Collection']
        active = form_filter.cleaned_data['active']
        inactive = form_filter.cleaned_data['inactive']
        type_filter = form_filter.cleaned_data['Type']
        
        
        
            
        
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'
        writer = csv.writer(response)
        
        
        
        
        writer.writerow(['collection',
                            'id',
                            'item_name',
                            'item_desc',
                            'status',
                            'graded',
                            'grader',
                            'grade',
                            'CAC',
                            'condition',
                            'mint',
                            'type_name',
                            'classification'
                            'category',
                            'metal',
                            'metal_weight',
                            'purity',
                            'recycled',])
        for i in collections:
            
            #needs some logic in here to filter inactive/active etc
            items = Item.objects.filter(collection=i,user=user,type__in=type_filter)
            for item in items:
                
                type = Type.objects.get(id=item.type_id)
                
                writer.writerow([i,
                                item.id,
                                item.item_name,
                                item.item_desc,
                                item.status,
                                item.graded,
                                item.grader,
                                item.grade,
                                item.CAC,
                                item.condition,
                                item.mint,
                                # type.type_name,
                                type.classification,
                                type.category,
                                # type.metal,
                                # type.metal_weight,
                                # type.purity,
                                type.recycled,])
    
                
                
        return response #uncomment this to make the CSV available on download. otherwise form stays the same. 
        content = {  
                    'form' : form,
                    'form_f' : form_filter,
                  }
        return render(request, 'inventory/export.html', content)
    else:
        form = ExportForm(name=user_obj)
        form_filter = ExportFilterForm(name=user_obj)
        
        content = {  
                    'form' : form,
                    'form_f' : form_filter,
                  }
        return render(request, 'inventory/export.html', content)