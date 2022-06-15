from django.http import HttpResponse
from django.shortcuts import redirect


def userNotLogged(view_func):
    def wrapper_fun(req,*args,**kwargs):
        if req.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(req,*args,**kwargs)
    return wrapper_fun


def allowedUsers(allowedGroups=[]):
    def decorator(view_func):
        def wrapper_func(request , *args,**kwargs): 
          group = None
          if request.user.groups.exists():
               group =  request.user.groups.all()[0].name
          if group in allowedGroups:
               return view_func(request , *args,**kwargs)
          else:
                return redirect('user')
        return wrapper_func
    return decorator

def forAdmins(view_func): 
        def wrapper_func(request , *args,**kwargs): 
            group = None
            if request.user.groups.exists():
               group =  request.user.groups.all()[0].name
            if group == 'admin':
               return view_func(request , *args,**kwargs)
            if group == 'customer':
                return redirect('user') 
            
        return wrapper_func 

