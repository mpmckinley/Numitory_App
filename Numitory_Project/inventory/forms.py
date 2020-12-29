from django.contrib.auth.models import User
from django.db.models import fields
from django.forms import ModelForm
from django.contrib.auth.forms import UserChangeForm
from django import forms
from .models import Item, Collection, Transaction, Type

class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]

class ItemCreateForm(ModelForm):
    class Meta:
        model = Item
        fields = [
            'item_name',
            'item_desc',
            'collection',
            'type',
            'status',
        ]
    
    item_desc = forms.CharField(
        widget=(
            forms.Textarea(
                attrs={
                    'rows':2}
            )
        )
    )

    def __init__(self, user, **kwargs):
        super(ItemCreateForm, self).__init__(**kwargs)
        self.fields['type'].queryset = Type.objects.filter(user=user)
        self.fields['collection'].queryset = Collection.objects.filter(user=user)

class TypeCreateForm(ModelForm):
    class Meta:
        model = Type
        fields = [
            'type_name',
            'type_desc',
            'category',
        ]
class CollectionCreateForm(ModelForm):
    class Meta:
        model = Collection
        fields = [
            'coll_name',
            'coll_desc',
        ]

class TransactionCreateForm(ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'date',
            'direction',
            'tran_quantity',
            'tran_value',
        ]