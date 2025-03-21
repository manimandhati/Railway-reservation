from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
  path('',views.home,name="home"),
  path('signup',views.signup,name="signup"),
  path('signin',views.signin,name="signin"),
  path('signout',views.signout,name="signout"),
  path('activate/<uidb64>/<token>',views.activate,name="activate"),
  path('search',views.search,name="search"),
  path('show',views.show,name="show"),
  path('add',views.add,name="add"),
  path('booking',views.booking,name="booking"),
  path('bookform/',views.bookform,name="booking"),
  path('mybookings',views.mybookings,name="mybookings"),
  path('makepayment',views.makepayment,name="makepayment")
]