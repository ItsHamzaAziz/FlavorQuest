from django.urls import path
from . import views

urlpatterns = [
    path('/register', views.register, name='register'),
    path('/login', views.log_in, name='login'),
    path('/logout', views.log_out, name='logout'),
    path('/account-details', views.account_details, name='account_details'),
    path('/edit-account', views.edit_account, name='edit_account'),
]

