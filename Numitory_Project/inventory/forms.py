from django.contrib.auth.models import User
from django.db.models import fields
from django.forms import ModelForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.hashers import make_password, check_password
from django import forms
from .models import Item, Collection, Transaction, Type

class UserChangeForm(forms.ModelForm):
    password_confirmation = forms.CharField(
        label='Confirm Password',
        max_length=70,
        widget=forms.PasswordInput(),
        required=False,
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].required=False
        
    def clean_password(self):
        data = self.cleaned_data['password']
        data = make_password(data)
        return data
		
    def clean(self):
        cleaned_data = super(UserChangeForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("password_confirmation")
        if(password!="" and confirm_password!=""):
            # raise forms.ValidationError(confirm_password)
            if(check_password(confirm_password,password)==False):
                raise forms.ValidationError(
                    "password and confirm_password does not match"
                )
			
    class Meta:
        password = forms.CharField(widget=forms.PasswordInput(),required=False)
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
			'password'
        ]
        widgets = {
            'password': forms.PasswordInput()
        }
		
# class UserChangeFormPassword(UserChangeForm):
    # confirm_password = forms.CharField(widget=forms.PasswordInput())
    # class Meta(UserChangeForm.Meta):
        # fields = UserChangeForm.Meta.fields + ['confirm_password',]
    

class ItemCreateForm(ModelForm):
    class Meta:
        model = Item
        fields = [
            'item_name',
            'item_desc',
            'collection',
            'type',
            'status',
<<<<<<< HEAD
            'image'
=======
            'graded',
            'grade',
            'condition',
>>>>>>> fcb4b3a4187a65f021ed93dfc960120a2ffa3b2d
        ]
    
    item_desc = forms.CharField(
        widget=(
            forms.Textarea(
                attrs={
                    'rows':1}
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
            'metal',
            'metal_weight',
            'purity',
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