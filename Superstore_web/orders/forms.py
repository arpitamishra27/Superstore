from django.forms import ModelForm, Form, formset_factory, modelformset_factory
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import authenticate
from .models import *
from django.contrib.auth.forms import UserCreationForm

SEGMENTS = (
        ("Consumer", "Consumer"),
        ("Corporate", "Corporate")
    )
    
class LoginForm(ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput
        }
        help_texts = {
            'username':None
        }

    def clean(self):
        super(LoginForm,self).clean()

        username = self.cleaned_data.get('username').lower()
        password = self.cleaned_data.get('password')

        if not authenticate(username=username,password=password):
            self._errors['username'] = self.error_class(['Username or Password is Incorrect'])
        return self.cleaned_data

class SendEmail(ModelForm):
    class Meta:
        model = User
        fields = ['email']

    def clean(self):
        super(SendEmail,self).clean()
        email = self.cleaned_data.get('email')
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
             self._errors['email'] = self.error_class([
                'email does not exists'])
                
        return self.cleaned_data

class CustomerForm(ModelForm):
    
    class Meta:
        model = mm_customer
        fields = ['first_name', 'last_name', 'segment']
        widget = {
            'segment':forms.ChoiceField(choices = SEGMENTS)
        }

class ProductForm(ModelForm):
    class Meta:
        model = mm_product
        exclude = ('product_id',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sub_category_id'].queryset = mm_sub_category.objects.none()

        if 'category_id' in self.data:
            try:
                category_id = int(self.data.get('category_id'))
                self.fields['sub_category_id'].queryset = mm_sub_category.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['sub_category_id'].queryset = mm_sub_category.objects.filter(category_id=self.instance.category_id)
        
AddProductFormSet = modelformset_factory(
    mm_order_product , fields=('product_id', 'quantity','discount','shipping_cost'), extra=1
)

class AddressForm(ModelForm):
    postal_code = forms.IntegerField()
    class Meta:
        model = mm_address
        exclude = ('address_id',)

class CategoryForm(ModelForm):
    class Meta:
        model = mm_category
        exclude = ('category_id',)

class SubCategoryForm(ModelForm):
    class Meta:
        model = mm_sub_category
        exclude = ('sub_category_id',)

class CreateUser(UserCreationForm):
    class Meta:
        model = User
        fields = [
                    'is_superuser', 
                    'username', 
                    'first_name', 
                    'last_name', 
                    'email', 
                    'password1', 
                    'password2'
                ]
        help_texts = {
                    'is_superuser': None,
                    'username': None, 
                    'first_name': None, 
                    'last_name': None,
                    'email': None, 
                    'password1' : None, 
                    'password2' : None, 
        }