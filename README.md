# WantON
 
WantON is a Flask server that responds to image text-messages with three different addresses of restaurants nearby that likely have the food that is depicted in the image. Powered by Twilio, Clarifai, and Yelp!

![WantON_Demo](http://i.imgur.com/kVMScgUl.jpg?1)


## Setup
#####\*WantON was implemented and tested in Python 3.5 only. Other versions of Python may not work.\*
<br />
Clone this repository with the following command in terminal.
```Shell
git clone https://github.com/bhernandez-cs/WantON.git
```
Within terminal and inside the project folder, install the necessary libraries and APIs that are required by WantON. A virtual environment is a good idea!
```Shell
pip install -r requirements.txt
```
Create a new file titled 'credentials.py' that will host your personal credentials for the Twilio API and the Clarifai API. Inside of your 'credentials.py' file should be the following:
```Python
#You can find/get Twilio credntials at https://www.twilio.com/console
account_sid = "YOUR TWILIO ACCOUNT SID"
auth_token = "YOUR TWILIO AUTH TOKEN"
my_twilio_number = "YOUR TWILIO PHONE NUMBER"

#You can find/get Clarifai credentials at https://developer.clarifai.com/account/applications/
my_clarifai_id = "YOUR CLARIFAI ID"
my_clarifai_secret = "YOUR CLARAFAI SECRET"

#You can find/get Yelp credentials at https://www.yelp.com/developers/v2/manage_api_keys
my_yelp_consumer_key = "YOUR YELP CONSUMER KEY"
my_yelp_consumer_secret = "YOUR YELP CONSUMER SECRET"
my_yelp_token = "YOUR YELP TOKEN"
my_yelp_token_secret = "YOUR YELP TOKEN SECRET"
```

## Usage
Start the Flask WantON server with the following command inside of the project folder in terminal.
```Shell
python WantON.py
```
In order to let Twilio find your server, you can use any of the following services.
<ul>
<li><a href="https://ngrok.com/">ngrok</a></li>
<li><a href="http://devcenter.heroku.com/articles/python">Heroku</a></li>
<li><a href="http://flask.pocoo.org/snippets/65/">Webfaction</a></li>
<li><a href="http://flask.pocoo.org/docs/deploying/">Apache,FastCGI, or uWSGI</a></li>
<li><a href="http://flask.pocoo.org/snippets/48/">Dotcloud</a></li>
</ul>

Once you have an <b>online</b> server endpoint, visit the settings for your Twilio phone number at https://www.twilio.com/console and enter your endpoint: 

![Setup_1](http://i.imgur.com/zxZOIzY.png)

Save these settings and turn your want ON!

## Drawbacks
 <ul>
 <li>Location for restaurant search is based off of the general area that a given phone number belongs to. Hard to get location data from a single text message.</li>
 <li>Only the first three Clarifai tags for a given image are used, which narrows the Yelp search well. However it may be less accurate as a result. </li>
</ul>
