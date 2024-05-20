from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile, Post, Course, Comment
from django.http import JsonResponse
from django.db.models import F

# Create your views here.
def index(request):
    user_posts = Post.objects.all().order_by('-publication_date')
    popular_posts = Post.objects.all().order_by('post_upvotes')[:5]
    post_vote_count = {posts.id: posts.post_upvotes - posts.post_downvotes for posts in user_posts}

    if request.method == 'POST':
        if 'bookmark' in request.POST:
            post_id = request.POST.get('post_id')
            post = get_object_or_404(Post, id=post_id)
            profile = request.user.profile

            if post in profile.bookmarks.all():
                profile.bookmarks.remove(post)
            else:
                profile.bookmarks.add(post)
            return JsonResponse({'message': 'Task Done!'})

        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        new_post = Post.objects.create(post_title=title, post_text=content, author=request.user.profile)
        Post.save(new_post)
        return redirect('index')
    else:
        return render(request, 'index.html', {"popular_posts": popular_posts,
                                              "user_posts": user_posts,
                                              "post_vote_count": post_vote_count,
                                              "user": request.user})


def signup(request):
    courses = Course.objects.all()
    if request.method == 'POST':
        display_name = request.POST.get('display_name', '')
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
                new_profile = Profile.objects.create(display_name=display_name, user=user_model, user_course=course)
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
    return render(request, 'post.html')


def discussion(request, post_title):
    post = get_object_or_404(Post, post_title=post_title)
    comments = Comment.objects.filter(post=post)
    if request.method == 'POST':
        if 'bookmark' in request.POST:
            post_id = request.POST.get('post_id')
            post = get_object_or_404(Post, id=post_id)
            profile = request.user.profile

            if post in profile.bookmarks.all():
                profile.bookmarks.remove(post)
            else:
                profile.bookmarks.add(post)
            return JsonResponse({'message': 'Task Done!'})

        comment = request.POST.get('content', '')
        new_comment = Comment.objects.create(comment_author=request.user.profile, comment_text=comment, post=post)
        Post.objects.filter(id=post.id).update(comment_count=F('comment_count') + 1)
        new_comment.save()
        return redirect('discussion', post_title=post_title)
    else:
        return render(request, 'discussion.html', {'post': post,
                                                   'comments': comments})


def bookmarked_posts(request):
    profile = request.user.profile
    bookmarks = profile.bookmarks.all()
    if 'bookmark' in request.POST:
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        profile = request.user.profile

        if post in profile.bookmarks.all():
            profile.bookmarks.remove(post)
        else:
            profile.bookmarks.add(post)
        return JsonResponse({'message': 'Task Done!'})

    return render(request, 'bookmarks.html', {"bookmarks": bookmarks})


def profile(request, username):
    user = User.objects.get(username=username)
    user_posts = Post.objects.all().filter(author=user.profile)
    profile = request.user.profile
    connected_users = user.profile.connected_users.all()
    if request.method == 'POST':
        if 'bookmark' in request.POST:
            post_id = request.POST.get('post_id')
            post = get_object_or_404(Post, id=post_id)
            profile = request.user.profile

            if post in profile.bookmarks.all():
                profile.bookmarks.remove(post)
            else:
                profile.bookmarks.add(post)
            return JsonResponse({'message': 'Task Done!'})

        connect_with = request.POST.get('profile_id')
        new_profile_connection = get_object_or_404(Profile, id=connect_with)
        my_profile = request.user.profile

        if new_profile_connection in profile.bookmarks.all():
            my_profile.connected_users.remove(new_profile_connection)
        else:
            my_profile.connected_users.add(new_profile_connection)

    return render(request, 'profile.html', {'user': user,
                                            'user_posts': user_posts,
                                            'connected_users': connected_users})
