import requests
import json
from .models import CarDealer
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from .models import DealerReview

def analyze_sentiment(text):
    # Replace 'YOUR_API_KEY' and 'YOUR_URL' with your actual Watson NLU API key and service URL
    api_key = 'YOUR_API_KEY'
    service_url = 'YOUR_URL'

    authenticator = IAMAuthenticator(api_key)
    nlu = NaturalLanguageUnderstandingV1(
        version='2021-08-01',
        authenticator=authenticator
    )
    nlu.set_service_url(service_url)

    response = nlu.analyze(
        text=text,
        features=Features(sentiment=SentimentOptions())
    ).get_result()

    sentiment = response.get('sentiment', {}).get('document', {}).get('label', 'neutral')
    return sentiment

def get_request(url, params=None, auth_key=None, **kwargs):
    headers = {'Content-Type': 'application/json'}
    
    # Include API key in headers if provided
    if auth_key:
        headers['apikey'] = auth_key

    response = requests.get(url, params=params, headers=headers, **kwargs)

    if response.status_code == 200:
        return response.json()
    else:
        # Handle the case where the request was not successful
        response.raise_for_status()

def analyze_review_sentiments(dealerreview, api_key):
    url = 'your_watson_nlu_api_url_here'  # Replace with your Watson NLU API URL
    # Assuming dealerreview has attributes text, version, features, and return_analyzed_text
    params = {
        "text": dealerreview.text,
        "version": dealerreview.version,
        "features": dealerreview.features,
        "return_analyzed_text": dealerreview.return_analyzed_text
    }

    # Make a call to the get_request method with the provided parameters
    response = get_request(url, params=params, auth_key=api_key)

    # Process the response as needed
    return response

def post_request(url, json_payload, **kwargs):
    """
    Make a POST request to the specified URL with JSON payload.

    Parameters:
    - url: The URL to make the request to.
    - json_payload: A Python dictionary-like object to be sent as the JSON payload.
    - kwargs: Additional keyword arguments for the request.

    Returns:
    - The response object.
    """
    response = requests.post(url, json=json_payload, params=kwargs, headers={'Content-Type': 'application/json'},
                             auth=HTTPBasicAuth('apikey', 'your_api_key_here'))
    
    # Check for successful response (status code 2xx)
    response.raise_for_status()
    
    return response

# def get_request(url, params=None, auth_key=None, **kwargs):
#     headers = {'Content-Type': 'application/json'}
    
#     # Include API key in headers if provided
#     if auth_key:
#         headers['apikey'] = auth_key

#     response = requests.get(url, params=params, headers=headers, **kwargs)

#     if response.status_code == 200:
#         return response.json()
#     else:
#         # Handle the case where the request was not successful
#         response.raise_for_status()


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list

# def get_dealers_from_cf(url, **kwargs):
#     results = []
#     # Call get_request with a URL parameter
#     json_result = get_request(url)
#     if json_result:
#         # Get the row list in JSON as dealers
#         dealers = json_result["rows"]
#         # For each dealer object
#         for dealer in dealers:
#             # Get its content in `doc` object
#             dealer_doc = dealer["doc"]
#             # Create a CarDealer object with values in `doc` object
#             dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
#                                    id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
#                                    short_name=dealer_doc["short_name"],
#                                    st=dealer_doc["st"], zip=dealer_doc["zip"])
#             results.append(dealer_obj)

#     return results

# WITH LATEST CODE ADJUSTMENTS-------------------------------------------
# def get_dealers_from_cf(url, **kwargs):
#     results = []
#     # Call get_request with a URL parameter
#     json_result = get_request(url)
#     if json_result and "rows" in json_result:
#         # Get the row list in JSON as dealers
#         dealers = json_result["rows"]
#         # For each dealer object
#         for dealer in dealers:
#             # Get its content in `doc` object
#             dealer_doc = dealer.get("doc", {})  # Use get to handle missing "doc" key gracefully
#             # Create a CarDealer object with values in `doc` object
#             dealer_obj = CarDealer(
#                 address=dealer_doc.get("address", ""),
#                 city=dealer_doc.get("city", ""),
#                 full_name=dealer_doc.get("full_name", ""),
#                 id=dealer_doc.get("id", ""),
#                 lat=dealer_doc.get("lat", ""),
#                 long=dealer_doc.get("long", ""),
#                 short_name=dealer_doc.get("short_name", ""),
#                 st=dealer_doc.get("st", ""),
#                 zip=dealer_doc.get("zip", "")
#             )
#             results.append(dealer_obj)

#     return results

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result and "rows" in json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer.get("doc", {})  # Use get to handle missing "doc" key gracefully
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(
                address=dealer_doc.get("address", ""),
                city=dealer_doc.get("city", ""),
                full_name=dealer_doc.get("full_name", ""),
                id=dealer_doc.get("id", ""),
                lat=dealer_doc.get("lat", ""),
                long=dealer_doc.get("long", ""),
                short_name=dealer_doc.get("short_name", ""),
                st=dealer_doc.get("st", ""),
                zip=dealer_doc.get("zip", "")
            )
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealer_id, api_key):
    params = {'dealerId': dealer_id}
    
    # Make a call to get_request with the specified arguments
    json_result = get_request(url, params=params)

    results = []
    
    if json_result and "rows" in json_result:
        # Get the row list in JSON as reviews
        reviews = json_result["rows"]
        
        # For each review object
        for review in reviews:
            # Get its content in `doc` object
            review_doc = review.get("doc", {})
            
            # Create a DealerReview object with values in `doc` object
            review_obj = DealerReview(
                dealership=review_doc.get("dealership", ""),
                name=review_doc.get("name", ""),
                purchase=review_doc.get("purchase", ""),
                review=review_doc.get("review", ""),
                purchase_date=review_doc.get("purchase_date", ""),
                car_make=review_doc.get("car_make", ""),
                car_model=review_doc.get("car_model", ""),
                car_year=review_doc.get("car_year", ""),
                sentiment="",  # Initialize sentiment as an empty string
                id=review_doc.get("id", "")
            )
            
            # Analyze sentiments and assign the result to the sentiment attribute
            review_obj.sentiment = analyze_review_sentiments(review_obj, api_key)
            
            results.append(review_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



