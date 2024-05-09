from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.index, name='index'),
    path('register/', views.signup, name='signup'),
    path('', views.signin, name='signin'),
    path('post/', views.post, name='post'),
    path('profile/<str:username>/', views.profile, name='profile'),
]
