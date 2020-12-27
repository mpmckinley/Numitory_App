from django.forms import ModelForm
from django import forms
from django.forms.fields import ChoiceField
from .models import Item, Collection, Type

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
class TypeCreateForm(ModelForm):
    class Meta:
        model = Type
        fields = [
            'type_name',
            'type_desc',
        ]
class CollectionCreateForm(ModelForm):
    class Meta:
        model = Collection
        fields = [
            'coll_name',
            'coll_desc',
        ]