###############################################################################
#
# Author: Gregory A. Bauer, Jasper Wong, Amy Robertson
# Email: bauergr@oregonstate.edu
# Course: CS467_400_W2021
#
# Description: Routes for news page
#
# Note:
#
# References:
# https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
###############################################################################

# Library modules
from flask import Blueprint, request, Response, redirect, render_template 
from flask import session, send_from_directory
from google.cloud import datastore
from requests_oauthlib import OAuth2Session
import json
import constants
from google.oauth2 import id_token
from google.auth import crypt
from google.auth import jwt
from google.auth.transport import requests
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from os.path import join, dirname, realpath
import random
import string
from google.cloud import storage
# User modules
from repository import NewsRepository
from forms.news_form import NewsForm
from OAuth import printSession

UPLOADS_PATH = join(dirname(realpath(__file__)), 'uploads/')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

bp = Blueprint('news', __name__)
client = datastore.Client()

###############################################################################

@bp.route('/news', methods=["GET"])
def news():
    printSession('***** NEWS *****')
    if 'sub' not in session:
        return "sub not in session."
    else:
        data = NewsRepository.all()
        for d in data:
            d['created'] = datetime.strftime(d['created'], "%B %d, %Y")
        return render_template('news.html', news=data)

###############################################################################

@bp.route('/add_news', methods=["GET"])
def add_news():
    printSession('***** ADD PROFILE *****')
    if 'isAdmin' not in session:
        return "isAdmin not in session."
    elif session['isAdmin'] is False:
        return "Not an admin account."
    else:

        form = NewsForm()
        return render_template('news_add_edit.html')

###############################################################################

@bp.route('/update_news/<key>', methods=["GET"])
def update_news(key):
    printSession('***** UPDATE POST *****')
    news = NewsRepository.get(key)
    print(news)
    # print(pet['type'])
    if 'isAdmin' not in session:
        return "isAdmin not in session."
    elif session['isAdmin'] is False:
        return "Not an admin account."
    else:
        return render_template('news_add_edit.html', pet=news)

###############################################################################

@bp.route('/store_news', methods=["POST"])
def store_news():
    # Instantiate AdminProfileForm class used for input validation
    form = NewsForm(request.form)
    if form.validate():
        # Create new 'news' entity in data store if no key provided
        if request.form['pet_key'] == '':
            NewsRepository.create(request.form)
        # Update 'news' entity if key provided
        else:
            NewsRepository.update(form=request.form, key=request.form['pet_key'])
        responseBody = {"success": True, "message": "Data Successfully saved"}
    else:
        errors = []
        for fieldName, errorMessages in form.errors.items():
            field = []
            print(fieldName)
            for err in errorMessages:
                print(err)
        responseBody = {"success": False, "message": "There are errors in the inputs"}
    return (json.dumps(responseBody), 200)

###############################################################################

@bp.route('/admin_news', methods=["GET"])
def news_admin():
    printSession('***** PROFILE ADMIN *****')
    if 'isAdmin' not in session:
        return "isAdmin not in session."
    elif session['isAdmin'] is False:
        return "Not an admin account."
    else:
        # Return all 'news' entities to populate 'admin_news.html'
        # Instantiate singleton NewsRepository class with member functions
        # See 'repository.py'
        data = NewsRepository.all()
        # print(data)
        for d in data:
            d['created'] = datetime.strftime(d['created'], "%Y-%m-%d")
        return render_template('news_admin.html', news=data)

###############################################################################

# Route to delete news post from datastore
@bp.route('/delete_news', methods=["POST"])
def delete_post():
    key = request.form['key']
    # Instantiate singleton NewsRepository class with member functions
    # See 'repository.py'
    NewsRepository.delete_news(key=key)
    responseBody = {"success": True, "message": "Deleted"}
    return (json.dumps(responseBody), 200)

###############################################################################


