from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, Response
from flask_login import login_required, current_user, login_user
from .models import User
from . import table, db
import json
import os
from datetime import datetime
import boto3
import requests
from werkzeug.utils import secure_filename
views = Blueprint('views', __name__)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

client_id = "2bp5jt844uiegflc62v3f5h22o"
client_secret = "14f2vgb5s5k1r6pbgtdh7d18p9hdosbcru43f4terj5g81litdgr"
s3 = boto3.client('s3',
            region_name='eu-central-1',
            aws_access_key_id='AKIARG535AD7AZAREKBU',
            aws_secret_access_key='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')

s33 = boto3.resource('s3',
            region_name='eu-central-1',
            aws_access_key_id='AKIARG535AD7AZAREKBU',
            aws_secret_access_key='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')

client = boto3.client('cognito-idp', 
                    region_name='eu-central-1',
                    aws_access_key_id='AKIARG535AD7AZAREKBU',
                    aws_secret_access_key='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')

clients3 = boto3.client('s3', 
                    region_name='eu-central-1',
                    aws_access_key_id='AKIARG535AD7AZAREKBU',
                    aws_secret_access_key='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')

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def add_extension(filename):
    return '.' + filename.rsplit('.', 1)[1].lower() 

@views.route('/', methods=['GET', 'POST'])
def login():

    
    #return redirect(url_for('views.home'))
    token_url = "https://interviewproject.auth.eu-central-1.amazoncognito.com/oauth2/token"
    callback_uri = "https://awsinterviewprojectapp.herokuapp.com/"
    # OVO PROMENI KADA STAVLJAS NA EBEANSTALK
    #callback_uri = "http://localhost:5000/"
    print('working')
    code = request.values.get('code')
    #print(code)
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
    #print(response.json())
    access_token = (response.json()).get('access_token')
    if(access_token != None):
        responseNew = client.get_user(
            AccessToken = access_token
        )
        dict = list(responseNew.values())
        email = dict[1][2].get('Value')
        #email = 'nekitamomail@gmail.com'
        print(email)
    
        user = User.query.filter_by(email=email).first()
        if not user:
            new_user = User(email=email)
            db.session.add(new_user)
            db.session.commit()
            user = new_user
        if not current_user.is_authenticated:
            login_user(user, remember=True)
    
        return redirect(url_for('views.home'))

    return render_template("base.html", user=current_user)

@views.route('/loggedin', methods=['GET', 'POST'])
def home():
    # ovde treba da se uradi nesto ako emial nije validan i ako nema @ u sebi, onda sam nasao
    # pogresnu vrednost

    #return render_template("home.html", user=current_user)
    
    email = current_user.email
    #flash(email)
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
                'age': {},
                'image_name': {}
            }
        )
        city = None
        phone_number = None
        employer = None
        name = None
        birthday = None
        jobtitle = None
        age = None
        image_name = None
    else:
        lista = list(respondedItem.values())
        city = lista[0]
        image_name = lista[1]
        phone_number = lista[2]
        employer = lista[3]
        name = lista[5]
        birthday = lista[6]
        jobtitle = lista[7]
        age = lista[8]

    
    if request.method == 'POST':
        flash('Your account has been updated!')

        city = request.form.get('city')
        name = request.form.get('name')
        birthday = request.form.get('birthday')
        age = request.form.get('age')
        jobtitle = request.form.get('jobtitle')
        employer = request.form.get('employer')
        phone_number = request.form.get('phone_number')
        

        # update picture
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '' and file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(filename)
                print("s3bucket")
                image_name = email + add_extension(filename)
                s3.upload_file(
                    Bucket = "s3websitephotos",
                    Filename = filename,
                    Key = image_name
                )
                os.remove(filename)
            elif not allowed_file(file.filename) and file.filename != '':
                flash('Wrong picture format. It must be one of the following: ' + 'png, jpg, jpeg, gif')

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
                    'image_name': image_name
            }
        )
    
    return render_template("home.html", user=current_user, email = email, city = city, name = name, birthday = birthday, age = age, jobtitle = jobtitle, employer = employer, phone_number = phone_number)

@views.route('/downloadImage', methods=['POST'])
def download_image():
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
    if respondedItem != None:
        lista = list(respondedItem.values())
        city = lista[0]
        image_name = lista[1]
        phone_number = lista[2]
        employer = lista[3]
        name = lista[5]
        birthday = lista[6]
        jobtitle = lista[7]
        age = lista[8]
        #print(image_name)
        file_name = "profileImage" + add_extension(image_name)
        #s33.Bucket('s3websitephotos').download_file(Key = image_name, Filename = file_name)
        file = s3.get_object(Bucket='s3websitephotos', Key=image_name)
        # return Response(
        #     file['Body'].read(),
        #     mimetype='image/jpg',
        #     headers={"Content-Disposition": "attachment;filename=test.jpg"}
        # )

        return clients3.generate_presigned_url('get_object',
                                     Params={'Bucket': 's3websitephotos', 'Key': image_name},
                                     ExpiresIn=60)
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