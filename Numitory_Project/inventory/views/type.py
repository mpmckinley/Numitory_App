from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator

from ..forms import TypeCreateForm
from ..models import Type, Item


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
        except ValueError as ve:
            print("ve", ve)
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
            print("errors", form.errors)
            form.save()
            return redirect('inventory:typeinv')
        except ValueError as ve:
            return render(request, 'inventory/typedetail.html', {
                'type': type,
                'form': TypeCreateForm(),
                'error': 'You have some bad data in there, try again',
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