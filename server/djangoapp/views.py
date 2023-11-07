from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import AuthenticationForm
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from .forms import UserRegisterForm

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
def about_view(request):
    return render(request, 'djangoapp/about.html')

# Create a `contact` view to return a static contact page
#def contact(request):

def contact_view(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
# def login_request(request):
#     return render(request, 'djangoapp/registration/login.html')
def login_request(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp')
        else:
            messages.error(request, "There was an error logging in, please try again.")
            return redirect('djangoapp')
    else:
        return render(request, 'djangoapp/login.html')
	

# Create a `logout_request` view to handle sign out request
# def logout_request(request):


# Create a `registration_request` view to handle sign up request
# def registration_request(request):
def registration_request(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('djangoapp/login.html')
    else:
        form = UserRegisterForm()  # Move this line to the 'else' block
    return render(request, 'djangoapp/registration.html', {'form': form})



# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

