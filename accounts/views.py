from django.shortcuts import render,redirect
from django.contrib import messages
from . import models as m
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from . import forms as f
from datetime import datetime

# Create your views here.
# logged in user cannot go to login page
def anonymous_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('home'))
        return view_func(request, *args, **kwargs)
    return wrapped_view

# sign up view
@anonymous_required
def signup_view(request):
    if request.method == 'POST':
        form = f.CustomUserCreationForm(request.POST)
        print(request.POST)
        if form.is_valid():
            user = form.save()
            form.save_m2m()
            login(request, user)
            return redirect('home')
        else:
            # Form is invalid, display error messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = f.CustomUserCreationForm()
    return render(request, 'signup.html',{'form':form})

# login view
@anonymous_required
def login_view(request):
    if request.method == 'POST':
        form = f.CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # print('form is valid')
            user = form.get_user()
            login(request, user)
            # Redirect to your homepage
            return redirect('home')
        else:
            # Form is invalid, display error messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = f.CustomAuthenticationForm()
    return render(request, 'login.html',{'form':form})

# editing route
@login_required(login_url='/accounts/')
def edit_profile(request):
    user = request.user
    data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'mobile_number': user.mobile_number,
        'dob': user.dob,
        'username': user.username,
        'email': user.email,
        'user_hobbies': user.hobbies.all(),
    }
    # dob_datetime = datetime.strptime(user.dob, '%b. %d, %Y')
    formatted_dob = user.dob.strftime('%Y-%m-%d')
    all_hobbies = m.Hobby.objects.all()
    return render(request, 'profile.html', {'data': data,'all_hobbies':all_hobbies,'formatted_dob':formatted_dob})

# logout view it ends sessions
def logout_view(request):
    logout(request)
    return redirect('login_account')