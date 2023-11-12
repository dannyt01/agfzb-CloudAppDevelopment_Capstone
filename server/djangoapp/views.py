from django.shortcuts import render, redirect, get_object_or_404
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
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, analyze_sentiment
# from .restapis import get_reviews_for_dealer
# from .models import DealerReview
from .restapis import post_request
from datetime import datetime

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
    if request.method == "GET":
        url = "https://dec6c135-621d-4bc2-a849-35a162eba40d-bluemix.cloudantnosqldb.appdomain.cloud/dealerships/dealer-get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)
    
def get_reviews(request):
    if request.method == "GET":
        url = "https://dec6c135-621d-4bc2-a849-35a162eba40d-bluemix.cloudantnosqldb.appdomain.cloud/reviews/review-get"
        reviews = get_reviews_from_cf(url)
        
        # Process reviews and update sentiment
        for review in reviews:
            sentiment = analyze_sentiment(review.review)
            review.sentiment = sentiment
            review.save()

        # Return a list of reviews with updated sentiment
        return HttpResponse("Sentiment analysis completed.")
    

def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        # Assuming you have the cloud function URL for getting dealer reviews
        url = "https://dec6c135-621d-4bc2-a849-35a162eba40d-bluemix.cloudantnosqldb.appdomain.cloud/dealerships/review-get"
    
    # Get reviews from the URL
    reviews = get_dealer_reviews_from_cf(url, dealer_id, 'your_api_key_here')
    
    # Create a list to store review details
    review_details = []
    
    # Iterate through each review and get details
    for review in reviews:
        review_detail = f"Review ID: {review.id}, Name: {review.name}, Purchase: {review.purchase}, " \
                        f"Review: {review.review}, Sentiment: {review.sentiment}"
        review_details.append(review_detail)
    
    # Join the review details into a string
    result = '\n'.join(review_details)
    
    # Return the result as an HttpResponse
    return HttpResponse(result)

def add_review(request, dealer_id):
    """
    Add a review for a specific dealer.

    Parameters:
    - request: The HTTP request object.
    - dealer_id: The ID of the dealer for which the review is being added.

    Returns:
    - HttpResponse indicating success or failure.
    """
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return HttpResponse("Error: User must be authenticated to add a review.", status=403)

    # Get the dealer object
    dealer = get_object_or_404(YourDealerModel, pk=dealer_id)  # Replace YourDealerModel with the actual model for dealers

    # Create a dictionary for the review
    review = {
        "time": datetime.utcnow().isoformat(),
        "name": request.user.username,  # Assuming you want to use the username of the authenticated user
        "dealership": dealer_id,
        "review": "This is a great car dealer",  # Replace with the actual review text
        # Add other attributes as needed based on your cloud function
    }

    # Make a POST request to the review-post cloud function
    try:
        response = post_request("https://dec6c135-621d-4bc2-a849-35a162eba40d-bluemix.cloudantnosqldb.appdomain.cloud", json_payload=review)
        response.raise_for_status()
        return HttpResponse("Review added successfully!", status=201)
    except Exception as e:
        return HttpResponse(f"Error adding review: {str(e)}", status=500)
    
def add_review(request, dealer_id):
    """
    Add a review for a specific dealer.

    Parameters:
    - request: The HTTP request object.
    - dealer_id: The ID of the dealer for which the review is being added.

    Returns:
    - HttpResponse indicating success or failure.
    """
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return HttpResponse("Error: User must be authenticated to add a review.", status=403)

    # Get the dealer object
    dealer = get_object_or_404(YourDealerModel, pk=dealer_id)  # Replace YourDealerModel with the actual model for dealers

    # Create a dictionary for the review
    review = {
        "time": datetime.utcnow().isoformat(),
        "name": request.user.username,  # Assuming you want to use the username of the authenticated user
        "dealership": dealer_id,
        "review": "This is a great car dealer",  # Replace with the actual review text
        # Add other attributes as needed based on your cloud function
    }

    # Create a dictionary for the JSON payload
    json_payload = {"review": review}

    # Make a POST request to the review-post cloud function
    try:
        response = post_request("https://dec6c135-621d-4bc2-a849-35a162eba40d-bluemix.cloudantnosqldb.appdomain.cloud", json_payload=json_payload, dealerId=dealer_id)
        response.raise_for_status()
        return HttpResponse(f"Review added successfully! Response: {response.text}", status=201)
    except Exception as e:
        return HttpResponse(f"Error adding review: {str(e)}", status=500)

# def get_dealerships(request):
#     context = {}
#     if request.method == "GET":
#         return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

