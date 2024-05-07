from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile


# Create your views here.
def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        password_confirmation = request.POST.get('password2', '')

        # check if a data field is empty
        if username == '' or email == '' or password == '' or password_confirmation == '':
            messages.info(request, 'All fields must have an input.')
            return redirect('signup')

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
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('signin')
        else:
            messages.info(request, 'Passwords do not match.')
            return redirect('signup')
    else:
        return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        if username == '' or password == '':
            messages.info(request, 'All fields must have an input.')
            return redirect('signin')

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
