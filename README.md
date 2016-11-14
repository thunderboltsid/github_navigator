Github Navigator
================
A barebones flask app built to toy around with the Github API.

Installation
------------
- Make sure virtualenv is installed: `pip3 install virtualenv`
- Create virtual environment: `python3 -m virtualenv env`
- Launch the virtual environment: `source env/bin/activate`
- Install requirements: `pip install -r requirements.txt`

Usage:
------
- Launch virtual environment: `source env/bin/activate`
- Launch the flask application:
	* `python application.py` for the unauthorized version
	* `GITHUB_CLIENT_ID=... GITHUB_CLIENT_SECRET=... python application.py` for the authorized version where `...` needs to be replaced by your client id and client secret. The unauthorized API is rate limited so it's highly suggested that the authorized API is used. In order to get the client ID and the client secret, please create a github oauth application.
- GET `localhost:5000/navigator?search_term=arrow` where `arrow` is the search term.