# define a function to get the data from the ticket master API 

#import libraries
import requests
import json
import time
import os 


def get_events(endpoint,api_key,country_code,segment_name,page_number):
    """
    Get event ID from ticket master .
    Args:
        endpoint: provided endpoint to get data
        api_key: authorization key required
        country_code : parameter to filter events
        segment : filter parameter
        page_number : parse through each page
            
    Returns:
        response: response object from the requests library.
    """
    URL = f"https://app.ticketmaster.com{endpoint}.json?countryCode={country_code}&apikey={api_key}&segmentName={segment_name}"
    payload = {}
    headers = {
        'Access-Control-Allow-Headers':'origin, x-requested-with, accept'}

    response = requests.request("GET", URL, headers=headers, data=payload)
   
    return response

# Get data from FourSquare API

def get_venues_fs(venue,latitude, longitude,FOURSQUARE_KEY):
    """
    Get venues from foursquare with coordinates.
    Args:
        latitude (float): latitude for query (must be combined with longitude)
        longitude (float): longitude for query (must be combined with latitude)
        venue(string):A string to be matched against all content for this place
        FOURSQUARE_KEY: authorization key
    Returns:
        response: response object from the requests library.
    """
    
    URL = 'https://api.foursquare.com/v3/places/search'
    # Prepare parameters for the API request
    params = {
        'll': f'{latitude},{longitude}',  # latitude and longitude
        'radius': 2000,  # radius around the location
        'query':f'{venue}'
            }
    headers = {
        "Accept": "application/json",
        "Authorization": FOURSQUARE_KEY
                }

    response = requests.get(URL,params=params,headers=headers)
    return response
    
# Get data from Yelp API 

def get_venues_yelp(latitude,longitude,API_key):
    """
    Get venues from foursquare with coordinates.
    Args:
        latitude (float): latitude for query(longitude is required) 
        longitude (float): longitude for query (latitude is required)
        radius (integer): radius limitation for query
        match_threshold(string) :none: Do not apply any match quality threshold; all potential business matches will be returned.
                                default: Apply a match quality threshold such that only very closely matching businesses will be returned.
                                strict: Apply a very strict match quality threshold.
        limit(int): max data points pulled
            
    Returns:
        response: response object from the requests library.
    """
    URL = 'https://api.yelp.com/v3/businesses/search'
    # Prepare parameters for the API request
    params = {
        'latitude':latitude,
        'longitude':longitude,
        'radius': 900,
        'match_threshold':'strict',
        'limit':20
        
            }
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer "+ API_key #need Bearer as a part of the string
                }
    response = requests.get(URL,params=params,headers=headers)
    return response

def get_business_insights(id,API_key):
    """
    Args:
        id(string): business id from yelp
    Returns:
        response: response object from the requests library.
    """
    URL = "https://api.yelp.com/v3/businesses/insights"
    params={
        'business_ids':id,
        'date_range_start':202301,
        'date_range_end':202402
        }
    headers={
        "Accept": "application/json",
        "Authorization": "Bearer "+ API_key #need Bearer as a part of the string
                }
    response = requests.get(URL,params=params,headers=headers)
    return response

def get_events_yelp(latitude,longitude,start_date,API_key):
    """
    Get events from ticketmaster with coordinates.
    Args:
        latitude (float): latitude for query(longitude is required) 
        longitude (float): longitude for query (latitude is required)
        start_date: date available from ticketmaster data
        limit(int): max data points pulled
            
    Returns:
        response: response object from the requests library.
    """
    URL = 'https://api.yelp.com/v3/events'
    # Prepare parameters for the API request
    params = {
        'latitude':latitude,
        'longitude':longitude,
        #'limit':
        'start_date':start_date
            }
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer "+ API_key #need Bearer as a part of the string
                }
    response = requests.get(URL,params=params,headers=headers)
    return response


def get_business_match(name,address,city,state,API_key):
    """
    Get events from ticketmaster with coordinates.
    Args:
        name (string): name of business
        address1(string): address of business
        city(string): city in which business 
        state(string): province of location
        Country(string): parameter for filter 
            
    Returns:
        response: response object from the requests library.
    """
    URL = 'https://api.yelp.com/v3/businesses/matches'
    # Prepare parameters for the API request
    params = {
        'name':name,
        'address1':address,
        'city':city,
        'state':state,
        'country':'CA',
        'match_threshold':'default'
        
            }
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer "+ API_key #need Bearer as a part of the string
                }
    response = requests.get(URL,params=params,headers=headers)
    return response


def get_reviews(id,API_key):
    """
    Get events from ticketmaster with coordinates.
    Args:
        business_id (string): business id retrieved from earlier API
            
    Returns:
        response: response object from the requests library.
    """
    URL = f'https://api.yelp.com/v3/businesses/{id}/reviews'
    # Prepare parameters for the API request
    params = {
        'business_id_or_alias':id,
        'limit':20,
        'sort_by':'newest'
        
            }
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer "+ API_key #need Bearer as a part of the string
                }
    response = requests.get(URL,params=params,headers=headers)
    return response