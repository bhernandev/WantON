#Importing flask variables for a server side application
from flask import Flask, request, redirect, session

#Importing the Twilio REST API, and twiml for building Twilio responses
from twilio.rest import TwilioRestClient
import twilio.twiml

#Importing Clarifai and their REST API
from clarifai.client import ClarifaiApi

#Importing Yelp and their API / Authentication protocol
import requests
import oauth2

#Importing the credentials for the various APIs used
import credentials

#Python module for parsing JSON
import json

#Session object makes use of 'a secret key'.
#SECRET_KEY = 'a secret key'

#Flask server side application setup
app = Flask(__name__)
app.config.from_object(__name__)

#Initialization of API clients for Twilio and Clarifai
twilio_api = TwilioRestClient(credentials.account_sid, credentials.auth_token)
clarifai_api = ClarifaiApi(credentials.my_clarifai_id, credentials.my_clarifai_secret)

def request_yelp(url, url_params=None):
    #Initialization of credential parameters for Yelp API
    consumer_key = credentials.my_yelp_consumer_key
    consumer_secret = credentials.my_yelp_consumer_secret
    token = credentials.my_yelp_token
    token_secret = credentials.my_yelp_token_secret
    url_params = url_params or {}

    #Making the API get request using the oauth2 python library using the previously initialized credential parameters
    consumer = oauth2.Consumer(consumer_key, consumer_secret)
    oauth_request = oauth2.Request(method="GET", url = url, parameters=url_params)
    oauth_request.update(
        {
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_timestamp': oauth2.generate_timestamp(),
            'oauth_token': token,
            'oauth_consumer_key': consumer_key
        }
    )
    token = oauth2.Token(token, token_secret)
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()

    #Returning the value of the API get request
    return requests.get(signed_url).json()

#Definition and routing of a view function for the endpoint of our Flask Server
@app.route("/", methods=['GET', 'POST'])
def search_picture():
    #Grabbing information from the user who sent a message to the Twilio number and storing in variables
    url_for_image = request.values.get('MediaUrl0')
    from_number = request.values.get('From')
    request_state = request.values.get('FromState')
    request_city = request.values.get('FromCity')
    request_zip = request.values.get('FromZip')
    request_location = request_city + ", " + request_state + ", " + request_zip

    #Creation and sending of the initial message sent back to the user who put in the request
    message_init_string = "The following restaurants near " + request_location + " were found based on your image! :"
    message_init = twilio_api.messages.create(to=from_number, from_=credentials.my_twilio_number, body=message_init_string)

    #Using the Clarifai client to get the tags for the image that was sent in
    result = clarifai_api.tag_image_urls(url_for_image)
    tags_for_picture = result['results'][0]['result']['tag']['classes']

    search_text = "restaurant " #Adds 'restaurant' to the search, so that we dont get back anything other than restaurants!
    for i in range(3): search_text += (tags_for_picture[i] + ", ") #Adds the first three tags from the Clarifai tagging to the search

    #Initialization of parameters for searching with the Yelp API
    yelp_params = {
        'term': search_text,
        'location': request_location
    }

    yelped_businesses = request_yelp("http://api.yelp.com/v2/search", yelp_params) #Using the previously defined function to search yelp with the created yelp parameters
    business_address_1 = yelped_businesses['businesses'][0]['location']['address'][0] + "\n" + search_text #Text to use when sending back restuarant 1 to user
    business_address_2 = yelped_businesses['businesses'][1]['location']['address'][0] + "\n" + search_text #Text to use when sending back restuarant 2 to user
    business_address_3 = yelped_businesses['businesses'][2]['location']['address'][0] + "\n" + search_text #Text to use when sending back restuarant 3 to user

    twilio_api.messages.create(to=from_number, from_=credentials.my_twilio_number, body=business_address_1) #Creating and sending back restaurant 1 via Twilio
    twilio_api.messages.create(to=from_number, from_=credentials.my_twilio_number, body=business_address_2) #Creating and sending back restaurant 2 via Twilio
    twilio_api.messages.create(to=from_number, from_=credentials.my_twilio_number, body=business_address_3) #Creating and sending back restaurant 3 via Twilio

    return "OK" #Flask requires a return value from all view functions

if __name__ == "__main__":
    app.run(debug=True)
