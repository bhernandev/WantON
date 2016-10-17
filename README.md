# WantON
 
This is a Flask server that responds to image text-messages with three different addresses of restaurants nearby that likely have the food that is depicted in the image. Powered by Twilio, Clarifai, and Yelp!

![WantON_Demo](http://i.imgur.com/kVMScgU.jpg?1)

## Setup
#####\*WantON was implemented and tested in Python 3.5 only. Other versions of Python may not work.\*
<br />
Clone this repository with the following command in terminal
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
To be added

## Drawbacks
To be added
