from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user, login_user
from .models import User
from . import table, db
import json
from datetime import datetime
import boto3
import requests
views = Blueprint('views', __name__)

client_id = "2bp5jt844uiegflc62v3f5h22o"
client_secret = "14f2vgb5s5k1r6pbgtdh7d18p9hdosbcru43f4terj5g81litdgr"

@views.route('/', methods=['GET', 'POST'])
def login():
    token_url = "https://interviewproject.auth.eu-central-1.amazoncognito.com/oauth2/token"
    callback_uri = "https://awsproject1.lostinstrings.rs/"
    # OVO PROMENI KADA STAVLJAS NA EBEANSTALK
    #callback_uri = "http://localhost:5000/"
    code = request.values.get('code')
    #flash(code)
    #code = '5d25a1c2-cb4b-491d-83ca-f824ce108d39'
    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    #flash(auth)
    params = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "code": code,
        "redirect_uri": callback_uri
    }
    response = requests.post(token_url, auth=auth, data=params)
    #flash(response.json())
    access_token = (response.json()).get('access_token')
    if(access_token != None):
        client = boto3.client('cognito-idp', 
                    region_name='eu-central-1',
                    aws_access_key_id='AKIARG535AD7AZAREKBU',
                    aws_secret_access_key='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')
        responseNew = client.get_user(
            AccessToken = access_token
        )
        dict = list(responseNew.values())
        email = dict[1][2].get('Value')
        #email = 'nekitamomail@gmail.com'

    
        user = User.query.filter_by(email=email).first()
        if not user:
            new_user = User(email=email)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
    
        return redirect(url_for('views.home'))

    return render_template("base.html", user=current_user)

@views.route('/loggedin', methods=['GET', 'POST'])
def home():
    # ovde treba da se uradi nesto ako emial nije validan i ako nema @ u sebi, onda sam nasao
    # pogresnu vrednost

    return render_template("home.html", user=current_user)
        
    email = current_user.email
    response = table.get_item(
            Key={
                'email': email
            }
        )
    try:
        respondedItem = response['Item']
    except:
        respondedItem = None
    if respondedItem == None:
        # create a new item in the database
        table.put_item(
            Item={
                'email': email,
                'city': {},
                'phone_number': {},
                'employer': {},
                'name': {},
                'birthday':{},
                'jobtitle': {},
                'age': {}
            }
        )
        city = None
        phone_number = None
        employer = None
        name = None
        birthday = None
        jobtitle = None
        age = None
    else:
        lista = list(respondedItem.values())
        city = lista[0]
        phone_number = lista[1]
        employer = lista[2]
        name = lista[4]
        birthday = lista[5]
        jobtitle = lista[6]
        age = lista[7]
    if request.method == 'POST':
        flash('Your account has been updated!')

        city = request.form.get('city')
        name = request.form.get('name')
        birthday = request.form.get('birthday')
        age = request.form.get('age')
        jobtitle = request.form.get('jobtitle')
        employer = request.form.get('employer')
        phone_number = request.form.get('phone_number')
        table.put_item(
            Item={
                    'email':email,
                    'city': city,
                    'name': name,
                    'birthday': birthday,
                    'age': age,
                    'jobtitle': jobtitle,
                    'employer': employer,
                    'phone_number': phone_number,
            }
        )

        # if len(note) < 1:
        #     flash('Note is too short!', category='error')
        # else:
        #     new_note = Note(data=note, user_id=current_user.id)
        #     db.session.add(new_note)
        #     db.session.commit()
        #     flash('Note added!', category='success')
    return render_template("home.html", user=current_user, email = email, city = city, name = name, birthday = birthday, age = age, jobtitle = jobtitle, employer = employer, phone_number = phone_number)



# @views.route('/delete-note', methods=['POST'])
# def delete_note():
#     note = json.loads(request.data)
#     noteId = note['noteId']
#     note = Note.query.get(noteId)
#     if note:
#         if note.user_id == current_user.id:
#             db.session.delete(note)
#             db.session.commit()
#     #return render_template("home.html", user=current_user)
#     return jsonify({})