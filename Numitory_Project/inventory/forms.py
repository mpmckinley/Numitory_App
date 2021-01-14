from django.contrib.auth.models import User,Group
from django.db.models import fields
from django.forms import ModelForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.hashers import make_password, check_password
from django import forms
from django.forms.widgets import HiddenInput, NumberInput
from .models import Item, Collection, Transaction, Type, UserExtended

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
        self.fields['password'].widget.attrs.update({'autocomplete': 'new-password'})
        
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
    user_type = forms.ModelChoiceField(queryset=Group.objects.all(),required=True)
    
    def __init__(self,user,**kwargs):
        super(ExtendedUserForm, self).__init__(**kwargs)
        if(user):
            if(len(Group.objects.filter(user=user))>0):
                self.initial['user_type']=Group.objects.filter(user=user)[0]
            else:
                self.initial['user_type']=''
    
    class Meta:
        model = User
        fields = ['user_type']
        
    def save(self, **kwargs):
        not_empty_data = [ k for k,v in self.cleaned_data.items() if (v and v!="")]
        self.instance.save(update_fields=not_empty_data)
        
    def clean(self):
        cleaned_data = super(ExtendedUserForm, self).clean()
        type = cleaned_data.get("user_type")
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
            'count',
            'type',
        ]

    def __init__(self, user, **kwargs):
        super(ItemCreateForm, self).__init__(**kwargs)
        self.fields['type'].queryset = Type.objects.filter(user=user)
        # self.fields['type_detl'].queryset = Type_Detl.objects.filter(type_id=id)
        self.fields['collection'].queryset = Collection.objects.filter(user=user)
        self.fields['item_desc'].widget.attrs = {'rows': 4}
        # ***Mint conditional choices based on Type selection
        # self.fields['mint'].queryset = Type.objects.filter(id=Type.id)

class TypeCreateForm(ModelForm):
    class Meta:
        model = Type
        fields = [
            'classification',
            'country',
            'category',
            # 'type_name',
            'type_desc',
            # 'type_dates',
            'mint',
            'face_value',
            'url_pcgs',
            'url_ngc',
            'url_other',
        ]

# class TypeDetlForm(ModelForm):
#     class Meta:
#         model = Type_Detl
#         fields = [
#             'var_name',
#             'var_desc',
#             'years',
#             'mint',
#             'comp',
#             'weight',
#             'precious_type',
#             'precious_purity',
#             'precious_weight',
#             'edge',
#             'mintage',
#             'url_pcgs',
#             'url_ngc',
#             'url_other',
#             'designer',
#             'recycled',
#         ]

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

class ExportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        #self.user is given to us with ExportForm(user=user.id) in our view
        self.user = kwargs.pop('name',None)
        super(ExportForm, self).__init__(*args, **kwargs)
        #We create a field called 'Collection' with ModelMultipleChoiceField
        #The choices will be Selected from Collection() ModelChoiceField
        #Using the user_id field and a user object. 
 
        self.fields['Collection'] = forms.ModelMultipleChoiceField(Collection.objects.filter(user_id__in=User.objects.filter(username=self.user)))
 
    class Meta:
        model = Collection
        field = ('Collection')
        exclude = ['id','user','coll_name','coll_desc','recycled']
        widgets = {
            'Collection': forms.Select(attrs={'size': 4,'style': 'width:40px'})   
        }
 
class ExportFilterForm(forms.Form):
 
 
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('name',None)
        super(ExportFilterForm, self).__init__(*args, **kwargs)
        #We repeat the same here but for Type() Model.
        #We allow the field to not be required. 
        self.fields['Type'] = forms.ModelMultipleChoiceField(Type.objects.filter(user_id__in=User.objects.filter(username=self.user)),required=False)
 
    active = forms.BooleanField(required=False)
    inactive = forms.BooleanField(required=False)