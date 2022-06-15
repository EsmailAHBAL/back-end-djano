from django.forms import ModelForm
from .models import Customer, Order
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class formOrder(ModelForm):
    class Meta :
        model= Order
        fields="__all__"
class formCustomer(ModelForm):
    class Meta :
        model= Customer
        fields="__all__"
        exclude=['user']

class createUser(UserCreationForm):
    class Meta :
        model= User
        fields=['username','email','password1','password2']