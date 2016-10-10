from flask import Flask, request, redirect, session
from twilio.rest import TwilioRestClient
from clarifai.client import ClarifaiApi
import credentials
import twilio.twiml
import json

# Session object makes use of a secret key.
SECRET_KEY = 'a secret key'

app = Flask(__name__)
app.config.from_object(__name__)
client = TwilioRestClient(credentials.account_sid, credentials.auth_token)

clarifai_api = ClarifaiApi(credentials.my_clarifai_id, credentials.my_clarifai_secret)

# List of known callers
callers = {
    "+19178365650": "Brian",
    "+13473240270": "Baby <3",
}

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond and greet the caller by name, with number of text messages sent between the two parties."""

    counter = session.get('counter', 0)

    counter += 1

    session['counter'] = counter

    from_number = request.values.get('From')
    if from_number in callers:
        name = callers[from_number]
    else:
        name = "Anon"

    url_for_image = request.values.get('MediaUrl0')

    result = clarifai_api.tag_image_urls(url_for_image)

    classes_of_whatever = result['results'][0]['result']['tag']['classes'][0]

    message = "The first tag of your picture is: " + classes_of_whatever + "."

    messagePicture = client.messages.create(to=from_number, from_=credentials.my_twilio_number, body=message, media_url=url_for_image)

    #message = "I will send back your picture in a moment"
    #resp = twilio.twiml.Response()
    #resp.message(message)
    #return str(resp)
    return ""

if __name__ == "__main__":
    app.run(debug=True)
