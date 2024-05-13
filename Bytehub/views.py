from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile, Post, Course


# Create your views here.
def index(request):
    user_posts = Post.objects.all().order_by('-publication_date')
    post_vote_count = {posts.id: posts.post_upvotes - posts.post_downvotes for posts in user_posts}
    return render(request, 'index.html', {"user_posts": user_posts, "post_vote_count": post_vote_count})


def signup(request):
    courses = Course.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        course_id = request.POST.get('course', '')
        password = request.POST.get('password', '')
        password_confirmation = request.POST.get('password2', '')

        if password == password_confirmation:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'The email you want to use is already associated with an account.')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'The username you want to use is already taken.')
                return redirect('signup')
            else:
                # create the user object after getting the form data and validating duplicates
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # create the profile of the user after authentication
                user_model = User.objects.get(username=username)
                course = Course.objects.get(id=course_id)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id, user_course=course)
                new_profile.save()
                return redirect('signin')
        else:
            messages.info(request, 'Passwords do not match!')
            return redirect('signup')
    else:
        return render(request, 'signup.html', {"courses": courses})


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('signin')
    else:
        return render(request, 'signin.html')


def post(request):
    if request.method == 'POST':
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        new_post = Post.objects.create()
    else:
        return render(request, 'post.html')


def profile(request, username):
    user = User.objects.get(username=username)
    return render(request, 'profile.html', {'user': user})
