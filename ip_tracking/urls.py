from django.urls import path
from . import views

urlpatterns = [
    path('login/authenticated/', views.login_authenticated, name='login_authenticated'),
    path('login/anonymous/', views.login_anonymous, name='login_anonymous'),
]
