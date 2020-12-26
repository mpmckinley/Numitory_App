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
        ]
    type_id = forms.ChoiceField(
        choices=[(type.id, type.type_name) for type in Type.objects.all()])
    collection_id = forms.ChoiceField(
        choices=[(collection.id, collection.coll_name) for collection in Collection.objects.all()])