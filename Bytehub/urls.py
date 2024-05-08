from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('post/', views.post, name='post'),
    path('profile/', views.profile, name='profile'),
]
