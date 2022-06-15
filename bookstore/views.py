import json
from django.forms.models import inlineformset_factory
from django.shortcuts import redirect, render
from django.http import HttpResponse
from hamcrest import none
from sqlalchemy import null
from django.contrib import messages

from bookstore.decorators import allowedUsers
from .decorators import allowedUsers, userNotLogged,forAdmins
from .filter import OrderFilter
from bookstore.form import formCustomer, formOrder,createUser
from bookstore.models import Book, Customer, Order
from django.contrib.auth import authenticate
from django.contrib.auth import login as lgn
from django.contrib.auth import logout as lgo
from django.contrib.auth.decorators import *
from django.contrib.auth.models import Group

import requests
from django.conf import settings



data = [{
    "name":'Esmail',
    "age":20
},
{
    "name":'Mohammed Amine',
    "age":22 
}]
def __page(req):
    return render(req, 'main.html')

@login_required(login_url='login')   
# @allowedUsers(allowedGroups=['admin']) 
@forAdmins
def __getData(req):
    customer = Customer.objects.all()
    order = Order.objects.all()
    t_order=order.count()
    p_order=order.filter(status = 'Pending').count()
    o_order=order.filter(status = 'Out In Order').count()
    d_order=order.filter(status = 'delivered').count()
    i_order=order.filter(status = 'In Progress').count()
    data = {'customer':customer
    ,'order':order
    ,'t_order':t_order
    ,'p_order':p_order
    ,'o_order':o_order,
    'i_order':i_order
    ,'d_order':d_order
    }
    return render(req,'Home.html',data)

def __getBooks(req):
    booksData=Book.objects.all()
    return render(req,'Book.html',{'books':booksData})

def __getCustomer(req,id):
    customer = Customer.objects.get(id=id)
    orders = customer.order_set.all()
    myfilter=OrderFilter(req.GET,queryset=orders)
    orders=myfilter.qs
    data = {
        'customer':customer,
        'orders':orders,
        'myfilter':myfilter
    }
    return render(req, 'Customer.html',data)
@allowedUsers(allowedGroups=['admin'])
def __create(req):
    form=formOrder()
    context={
        'form':form
    }
    if req.method =='POST':
        print(req.POST)
        form=formOrder(req.POST)
        if form.is_valid():
           form.save()
           return redirect('/home')
    return render(req,'Create.html',context)

@allowedUsers(allowedGroups=['admin'])
def __createc(req,id):
    orderFrom=inlineformset_factory(Customer,Order,fields=('bookId','status'))
    customer = Customer.objects.get(id=id)
    formset=orderFrom(queryset=Order.objects.none(),instance=customer)
    if req.method =='POST':
        formset=orderFrom(req.POST,instance=customer)
        if formset.is_valid():
           formset.save()
           return redirect('/home')
    context={'formset':formset}       
    return render(req,'myOrder.html',context)

@allowedUsers(allowedGroups=['admin'])
def __update(req,id):
    order = Order.objects.get(id=id)
    form = formOrder(instance=order)
    if req.method =='POST':
        print(req.POST)
        form=formOrder(req.POST,instance=order)
        if form.is_valid():
           form.save()
           return redirect('/home')
    data = {'form':form}
    return render(req,'Create.html',data)

@allowedUsers(allowedGroups=['admin'])
def __delete(req,id):
    order = Order.objects.get(id=id)
    if req.method =='POST':
        order.delete()
        return redirect('/home')
    data = {'order':order}
    return render(req,'Delete.html',data)
@userNotLogged
def __signup(req):
     
      form = createUser()
      if req.method=="POST":
        form=createUser(req.POST)
        if form.is_valid():
          username =form.cleaned_data.get('username')
          group=Group.objects.get(name="customer")
          user=form.save()   
          user.groups.add(group)
          messages.success(req,username +'Created  ✌')  
          return redirect('/login')  
        else:
            messages.error(req,'Try Again  🥺 ')
          
       
      context={'form':form}
      return render(req,'Signup.html',context)    

@userNotLogged
def __login(req):
        
    if req.method=='POST':
            username= req.POST.get('username')
            password= req.POST.get('password')  
            recaptcha_response = req.POST.get('g-recaptcha-response')
            data = {
                           'secret' : settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                         'response' : recaptcha_response
                       }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify',data=data)
            result = r.json()
            if result['success']:
                user=authenticate(req,username=username,password=password)
                if user is not None:
                    lgn(req,user)
                    return redirect('/home')
                else:
                    messages.info(req,'User Not Valid 🔒 ')
            else   :
               messages.info(req,'User Not Valid 🔒 ')
                
     
    return render(req,'Login.html')       

def __logout(req):
    lgo(req)
    return redirect('/login')   

@login_required(login_url='login') 
@allowedUsers(allowedGroups=['customer'])        
def __user(req):
    order = req.user.customer.order_set.all()
    print(order)
    return render(req,'user.html',{'orders':order})

@login_required(login_url='login')
def __user_profile(req):
    customer = req.user.customer
    form=formCustomer(instance=customer)
    if req.method == 'POST':
       form=formCustomer(req.POST,req.FILES,instance=customer) 
       if form.is_valid():
        form.save()
    data = {"form":form}
    return render(req,'user_profile.html',data)    