from flask import Flask, jsonify, redirect, url_for, session
import os
from authlib.integrations.flask_client import OAuth
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from api_helper_functions import parse_yahoo_response_to_xml, extract_fantasy_info
from data_base_helper_functions import update_or_create_user
from models import db, User

# Initialize Flask and OAuth
app = Flask(__name__)
app.secret_key = 'blue'  # Change this!

# change this to your Railway PostgreSQL URL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:54-GGB44bB1A-*5Cg16Dg**bb5gf2A*D@viaduct.proxy.rlwy.net:28341/railway'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

oauth = OAuth(app)
yahoo = oauth.register(
    name='yahoo',
    client_id= os.environ.get('YAHOO_CONSUMER_KEY'),
    client_secret= os.environ.get('YAHOO_CONSUMER_SECRET'),
    access_token_url='https://api.login.yahoo.com/oauth2/get_token',
    authorize_url='https://api.login.yahoo.com/oauth2/request_auth',
    api_base_url='https://api.login.yahoo.com/',
    client_kwargs={'scope': 'fspt-r'}
)

@app.route('/')
def index():
    return 'Welcome! <a href="/login">Login with Yahoo</a>'

@app.route('/login')
def login():
    redirect_uri = "https://alexball.up.railway.app//callback"
    return yahoo.authorize_redirect(redirect_uri)

@app.route('/callback')
def authorize():
    token = yahoo.authorize_access_token()
    session['token'] = token

    # Fetch user info from Yahoo
    response = yahoo.get('https://fantasysports.yahooapis.com/fantasy/v2/users;use_login=1/games;game_keys=nba.2023/leagues/teams')
    
    # Get and print the XML response
    xml_response = response.content.decode('utf-8')

    # Write the XML response to a file
    with open('yahoo_response.xml', 'w') as f:
        f.write(xml_response)

    
    xml_response = parse_yahoo_response_to_xml(response.content)
    extracted_user_info = extract_fantasy_info(xml_response)
    print(extracted_user_info)


    existing_user = update_or_create_user(session['token'], extracted_user_info)


    return f"{existing_user.team_name}"

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
    app.run(debug=True, port=os.getenv("PORT", default=5000))