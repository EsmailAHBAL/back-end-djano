
from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as authViews

urlpatterns = [
    path('home/',views.__getData ,name='home'),
    path('',views.__page),
    path('books/',views.__getBooks , name='books'),
    path('create/',views.__create , name='create'),
    path('signup/',views.__signup , name='signup'),
    path('login/',views.__login , name='login'),
    path('user/',views.__user , name='user'),
    path('logout/',views.__logout , name='logout'),
    path('createc/<str:id>',views.__createc , name='createc'),
    path('update/<str:id>',views.__update , name='update'),
    path('delete/<str:id>',views.__delete , name='delete'),
    path('customer/<str:id>',views.__getCustomer,name='customer'),
    path('profile/',views.__user_profile,name='user_profile'),
    
     path('reset_password/' ,authViews.PasswordResetView.as_view(template_name= "password_reset.html") , name="reset_password"),
     path('reset_password_sent/' ,authViews.PasswordResetDoneView.as_view() , name="password_reset_done"),
     path('reset/<uidb64>/<token>/' ,authViews.PasswordResetConfirmView.as_view() , name="password_reset_confirm"),
     path('reset_password_complete/' ,authViews.PasswordResetCompleteView.as_view() , name="password_reset_complete"),


]
