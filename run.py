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

# Session object makes use of a secret key.
SECRET_KEY = 'a secret key'

#Flask server side application setup
app = Flask(__name__)
app.config.from_object(__name__)

#Initialization of API clients for Twilio, Clarifai, and Yelp
twilio_api = TwilioRestClient(credentials.account_sid, credentials.auth_token)

clarifai_api = ClarifaiApi(credentials.my_clarifai_id, credentials.my_clarifai_secret)

def request_yelp(url, url_params=None):
    consumer_key = credentials.my_yelp_consumer_key
    consumer_secret = credentials.my_yelp_consumer_secret
    token = credentials.my_yelp_token
    token_secret = credentials.my_yelp_token_secret
    url_params = url_params or {}
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

    print(u'Querying {0} ...'.format(url))

    return requests.get(signed_url).json()

@app.route("/", methods=['GET', 'POST'])
def search_picture():

    url_for_image = request.values.get('MediaUrl0')
    from_number = request.values.get('From')
    request_state = request.values.get('FromState')
    request_zip = request.values.get('FromZip')
    request_location = request_state + " " + request_zip

    result = clarifai_api.tag_image_urls(url_for_image)

    tags_for_picture = result['results'][0]['result']['tag']['classes']

    message = "Your first three tags are: "

    for i in range(3): message += (tags_for_picture[i] + ", ")

    yelped_businesses = request_yelp("http://api.yelp.com/v2/search?location=Boston&term=food")

    business_address = yelped_businesses['businesses'][0]['location']['address'][0]

    messagePicture = twilio_api.messages.create(to=from_number, from_=credentials.my_twilio_number, body=business_address)

    return ""

if __name__ == "__main__":
    app.run(debug=True)
