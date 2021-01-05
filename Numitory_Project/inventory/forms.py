from django.contrib.auth.models import User
from django.db.models import fields
from django.forms import ModelForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.hashers import make_password, check_password
from django import forms
from django.forms.widgets import HiddenInput, NumberInput
from .models import Item, Collection, Transaction, Type,UserExtended

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
        if(data!=""):
            data = make_password(data)
        return data
		
    def clean(self):
        cleaned_data = super(UserChangeForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("password_confirmation")
        if(password!="" and confirm_password!=""):
            if(check_password(confirm_password,password)==False):
                raise forms.ValidationError(
                    "New password and confirm password do not match")
        elif(password!='' and confirm_password==''):
            raise forms.ValidationError(
                    "Please Confirm Your new password")
        elif(password=='' and confirm_password!=''):
            raise forms.ValidationError(
                    "Please Enter your Password if you want to Change the Password")
                    
    def save(self, **kwargs):
        not_empty_data = [ k for k,v in self.cleaned_data.items() if (v and v!="" and k!='password_confirmation')]
        self.instance.save(update_fields=not_empty_data)
    
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

class ExtendedUserForm(forms.ModelForm):
    class Meta:
        model = UserExtended
        fields = ['user_type']
        
    def save(self, **kwargs):
        not_empty_data = [ k for k,v in self.cleaned_data.items() if (v and v!="")]
        self.instance.save(update_fields=not_empty_data)
        
    def clean(self):
        cleaned_data = super(ExtendedUserForm, self).clean()
        type = cleaned_data.get("user_type")
        # print(type==None)
        if (type==None or type=='' or type==0):
            raise forms.ValidationError("User Type is Required")
        

class ItemCreateForm(ModelForm):
    class Meta:
        model = Item
        fields = [
            'item_name',
            'item_desc',
            'item_image',
            'status',
            'graded',
            'grader',
            'grader_id',
            'grade',
            'condition',
            'CAC',
            'mint',
            'type',
            'collection',
        ]

    def __init__(self, user, **kwargs):
        super(ItemCreateForm, self).__init__(**kwargs)
        self.fields['type'].queryset = Type.objects.filter(user=user)
        self.fields['collection'].queryset = Collection.objects.filter(user=user)
        self.fields['item_desc'].widget.attrs = {'rows': 5}
        # ***Mint conditional choices based on Type selection
        # self.fields['mint'].queryset = Type.objects.filter(id=Type.id)

class TypeCreateForm(ModelForm):
    class Meta:
        model = Type
        fields = [
            'type_name',
            'type_desc',
            'classification',
            'category',
            'metal',
            'metal_weight',
            'purity',
            'mint',
            'face_value',
            'url_pcgs',
            'url_ngc',
            'url_other',
            'recycled',
        ]

class CollectionCreateForm(ModelForm):
    class Meta:
        model = Collection
        fields = [
            'coll_name',
            'coll_desc',
        ]

class TransactionCreateForm(ModelForm):

    date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    class Meta:
        model = Transaction
        fields = [
            'date',
            'direction',
            'tran_quantity',
            'tran_value',
        ]

    # def __init__(self, *args, **kwargs):
    #     super(TransactionCreateForm, self).__init__(**kwargs)
    #     self.fields['tran_value_currency'].widget = HiddenInput()
