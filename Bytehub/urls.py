from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('home/', views.index, name='index'),
    path('register/', views.signup, name='signup'),
    path('', views.signin, name='signin'),
    path('post/', views.post, name='post'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('discussion/<str:post_title>/', views.discussion, name='discussion'),
    path('bookmarks/', views.bookmarked_posts, name='bookmarks'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/Bytehub'), name='logout'),
]
