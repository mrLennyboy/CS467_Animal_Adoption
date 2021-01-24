###############################################################################################################
#                                                                                                             #          
# Author: Gregory A. Bauer, Jasper Wong, Amy Robertson                                                                                    #
# Email: bauergr@oregonstate.edu                                                                              #
# Course: CS467_400_W2021                                                                                    #
# Sources: https://developers.google.com/identity/protocols/oauth2/web-server#httprest,                       #
#   https://stackoverflow.com/questions/17057191/redirect-while-passing-arguments,                            #
#   https://flask.palletsprojects.com/en/1.1.x/quickstart/,                                                   #
#   https://stackoverflow.com/questions/51262531/flask-context-variable-not-available-in-template/51262916    #
#                                                                                                             #  
#                                                                                                             #
###############################################################################################################

from flask import Blueprint, request, Response, redirect, render_template, session
import json
import requests
from requests_oauthlib import OAuth2Session
from google.oauth2 import id_token
from google.auth import crypt
from google.auth import jwt
from google.auth.transport import requests
from google.cloud import datastore
import constants
from datetime import datetime

bp = Blueprint('OAuth', __name__)
client = datastore.Client()

CLIENT_ID = r'939115278036-he2m51te7ohrp1m9r457nos1dbnh5u2o.apps.googleusercontent.com'
CLIENT_SECRET = r'LQQ_RyrsV-eA1uiuux0RrI7J'
SCOPES = ['openid', 'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile']
REDIRECT_URI = 'https://datingappforanimaladoption.wl.r.appspot.com/authorization'

OAUTH = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPES)

###############################################################################################################

@bp.route('/home', methods=['GET'])
def mainPage():
    
    return render_template('index.html')
    
###############################################################################################################

@bp.route('/admin', methods=['GET'])
def adminPage():
    
    return render_template('admin.html')
    
###############################################################################################################

@bp.route('/user', methods=['GET'])
def userPage():
    
    return render_template('user.html')
    
###############################################################################################################
    
@bp.route('/index', methods=['GET'])
def index():

    # This url renders a diaglog box to authenticate using google account
    authorization_url, state = OAUTH.authorization_url(
        'https://accounts.google.com/o/oauth2/auth',
        # access_type and prompt are Google specific extra
        # parameters.
        access_type="offline", prompt="select_account")
        
    return redirect(authorization_url)

###############################################################################################################
 
@bp.route('/authorization', methods=['GET'])
def callback():
  
    # After redirect from authentication, this route returns the authorization token
    token = OAUTH.fetch_token(
        # Token endpoint
        'https://accounts.google.com/o/oauth2/token',
        authorization_response=request.url,
        client_secret=CLIENT_SECRET)
        
    req = requests.Request()

    # Get email of authenticated user
    id_info = id_token.verify_oauth2_token(token['id_token'], req, CLIENT_ID)
    
    # Store token, sub, and email in session
    session['id_token'] = token['id_token']
    session['usr_email'] = id_info['email']
    session['sub'] = id_info['sub']

    #return "Your JWT is: %s" % token['id_token']
    #return "Your email is: %s" % id_info #['email']
    return redirect('/results')

###############################################################################################################   

@bp.route('/results', methods=['GET'])
def results():
    
    email = session['usr_email']
    jwt = session['id_token']
    sub = session['sub']
    
    # query all users in database
    query = client.query(kind=constants.users)
    results = list(query.fetch())
    
    # Check if user has account
    for r in results:
        try:
            # User already exists
            if r['uniqueID'] == sub:
                return render_template('results.html', email=email, jwt=jwt)
        except:
            pass
    
    # Record account creation date
    now = datetime.now()
    dt_string = now.strftime("%m/%d/%Y %H:%M:%S")   

    # Store user in database
    new_user = datastore.entity.Entity(key=client.key(constants.users))
    new_user.update({"uniqueID": sub, "email": email, "boats": None, "creation_date": dt_string, "last_modified": None})
    client.put(new_user)        
    
    return render_template('results.html', sub=sub, email=email, jwt=jwt)
    
############################################################################################################### 
                   