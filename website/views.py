from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db, table
import json
from datetime import datetime
import boto3
import requests
views = Blueprint('views', __name__)

client_id = "2bp5jt844uiegflc62v3f5h22o"
client_secret = "14f2vgb5s5k1r6pbgtdh7d18p9hdosbcru43f4terj5g81litdgr"

@views.route('/', methods=['GET', 'POST'])
def home():
    # if request.method == 'GET':
    #     token_url = "https://interviewproject.auth.eu-central-1.amazoncognito.com/oauth2/token"
    #     callback_uri = "http://localhost:5000/note"
    #     code = request.values.get('code')
    #     #code = '5d25a1c2-cb4b-491d-83ca-f824ce108d39'
    #     auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    #     params = {
    #         "grant_type": "authorization_code",
    #         "client_id": client_id,
    #         "code": code,
    #         "redirect_uri": callback_uri
    #     }
    #     response = requests.post(token_url, auth=auth, data=params)
    #     access_token = (response.json()).get('access_token')
    #     client = boto3.client('cognito-idp', 
    #                 region_name='eu-central-1',
    #                 aws_access_key_id='AKIARG535AD7AZAREKBU',
    #                 aws_secret_access_key='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')
    #     responseNew = client.get_user(
    #         AccessToken = access_token
    #     )
    #     flash(responseNew)
        

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
                    'email':'nekitamomail@gmail.com',
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

    return render_template("home.html", user=current_user)



@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    #return render_template("home.html", user=current_user)
    return jsonify({})