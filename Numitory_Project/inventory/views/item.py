from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models.aggregates import Count
from django.core.paginator import Paginator

from ..forms import ItemCreateForm, TransactionCreateForm
from ..models import Transaction, Item, Type


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
        trans_with_forms = [
            dict(trans=transaction, form=TransactionCreateForm(instance=transaction)) for transaction in trans
        ]

        total = Transaction.objects.filter(user=request.user, tran_item_id=item_pk).aggregate(Count('id'))

        # detail = Type.objects.filter(user=request.user, id=item.type_id)
        detail = get_object_or_404(Type, user=request.user, id=item.type_id)

        paginator = Paginator(trans_with_forms, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'inventory/itemdetail.html', {
            'item': item,
            'form': form,
            'trans': trans,
            'tranform': tranform,
            'trans_with_forms': trans_with_forms,
            'total': total,
            'detail': detail,
            'page_obj': page_obj,
            'page_title': 'Numitory - Item Detail'

        })
    print("request post", request.POST)
    if 'item' in request.POST:
        try:
            form = ItemCreateForm(data=request.POST, files=request.FILES, user=request.user, instance=item)
            form.save()
            print(form.data)
            return redirect('inventory:inventory')
        except ValueError:
            return render(request, 'inventory/itemdetail.html', {
                'item': item,
                'form': ItemCreateForm(user=request.user, instance=item),
                'tranform': TransactionCreateForm(),
                'error': 'You have some bad data in there, try again',
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
                'error': 'You had some bad data in your tran form, try again',
            })

    if 'edit_tran' in request.POST:
        transaction = get_object_or_404(Transaction, pk=request.POST["pk"])
        tranform = TransactionCreateForm(instance=transaction, data=request.POST)
        tranform.save()
        return redirect(request.path_info)


    # ***TRANSACTION DELETE
    pk = request.POST['pk']
    if request.method == 'POST' and 'delete' in request.POST:
        tran = get_object_or_404(Transaction, pk=pk)
        tran.delete()
        return redirect(request.path_info)

