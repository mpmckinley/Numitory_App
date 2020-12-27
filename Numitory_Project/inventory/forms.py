from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import UserChangeForm
from django import forms
from .models import Item, Collection, Type

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
        # collection = forms.ChoiceField(
        #     choices=[(x.id, x.coll_name) for x in Collection.objects.all()])
        #     # choices=[(x.id, x.type_name) for x in Collection.objects.filter(user_id=User.id)])
        # type = forms.ChoiceField(
        #     choices=[(x.id, x.type_name) for x in Type.objects.all()])
        fields = [
            'item_name',
            'item_desc',
            'collection',
            'type',
            'status',
        ]
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
        ]
class CollectionCreateForm(ModelForm):
    class Meta:
        model = Collection
        fields = [
            'coll_name',
            'coll_desc',
        ]