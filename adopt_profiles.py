###############################################################################################################
#
# Author: Gregory A. Bauer, Jasper Wong, Amy Robertson
# Email: bauergr@oregonstate.edu
# Course: CS467_400_W2021
#
# Description: Routes for profiles page. Profile card dynamic.
#
# Note:
#
#
# References: https://stackoverflow.com/questions/35444880/how-to-view-an-image-stored-in-google-cloud-storage-bucket
#             https://cloud.google.com/storage/docs/access-public-data#api-link
#             
# 
###############################################################################################################

from flask import Blueprint, request, Response, redirect, render_template, session, make_response
from google.cloud import datastore
from requests_oauthlib import OAuth2Session
import json
import constants
from google.oauth2 import id_token
from google.auth import crypt
from google.auth import jwt
from google.auth.transport import requests
from datetime import datetime
# User modules
from repository import *

#import requests
bp = Blueprint('adopt_profiles', __name__)
client = datastore.Client()

from OAuth import printSession

# bucket name for GCS public URL + subfolder
BUCKET_NAME = "datingappforanimaladoption.appspot.com/uploads/"

###############################################################################################################
@bp.route('/adopt_profiles', methods=["GET"])
def view_profile():
    if 'sub' not in session:
        return "Error: \'sub\' not in session!!!"
    elif request.method == 'GET':
        # Return all pet entities in the datastore to populate 'profiles.html'
        # Instantiate singleton PetDsRepository class with member functions -- see 'repository.py'
        data = PetDsRepository.all()

        # API Link accessing public data format https://storage.googleapis.com/BUCKET_NAME/OBJECT_NAME
        public_url = "https://storage.googleapis.com/" + BUCKET_NAME
        return render_template('adopt_profiles.html', pets=data, public_url=public_url)
    else:
        # redo temporary error response
        return "Error"



