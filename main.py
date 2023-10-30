from flask import Flask, jsonify, redirect, url_for, session, request
import os
from authlib.integrations.flask_client import OAuth
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from api_helper_functions import parse_yahoo_response_to_xml, extract_fantasy_info
from data_base_helper_functions import update_or_create_user
from models import db, User
import logging
from urllib.parse import quote
from werkzeug.middleware.proxy_fix import ProxyFix
import secrets


logging.basicConfig(level=logging.DEBUG)

original_url = "https://alexball.up.railway.app/callback"
encoded_url = quote(original_url, safe=':/')


# Initialize Flask and OAuth
app = Flask(__name__)
app.secret_key = 'blue'  # Change this!
app.wsgi_app = ProxyFix(app.wsgi_app)

# change this to your Railway PostgreSQL URL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:54-GGB44bB1A-*5Cg16Dg**bb5gf2A*D@viaduct.proxy.rlwy.net:28341/railway'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

oauth = OAuth(app)

yahoo = oauth.register(
    name='yahoo',
    client_id=os.environ.get('YAHOO_CONSUMER_KEY'),
    client_secret=os.environ.get('YAHOO_CONSUMER_SECRET'),
    server_metadata_url='https://api.login.yahoo.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'fspt-r openid email',
    },
)


@app.route('/')
def index():
    print(f"Consumer Key/Client ID: {os.environ.get('YAHOO_CONSUMER_KEY')}")
    print(f"Consumer Secret : {os.environ.get('YAHOO_CONSUMER_SECRET')} "  )
    return 'Welcome! <a href="/login">Login with Yahoo</a>'

@app.route('/login')
def login():
    redirect_uri = encoded_url
    state = secrets.token_urlsafe(16)
    session['state'] = state
    print(redirect_uri)
    print(f"State sent:{state}")
    return yahoo.authorize_redirect(redirect_uri, state=state)

@app.route('/callback')
def authorize():
    received_state = request.args.get('state')  # State received from Yahoo
    session_state = session.get('state')  # State you generated and saved in session
    
    # Verify the state
    if received_state is None or session_state is None or received_state != session_state:
        return 'State mismatch. Authorization failed.', 400

    try:
        token = yahoo.authorize_access_token()
        print(f"Size of token: {len(str(token))} bytes")
        print(token)
    except Exception as e:
        print(f"Exception: {e}")
        return str(e), 400
    
    
    session['token'] = token

    # Fetch user info from Yahoo
    response = yahoo.get('https://fantasysports.yahooapis.com/fantasy/v2/users;use_login=1/games;game_keys=nba.2023/leagues/teams')

    # Print the status code
    print(f"Yahoo API response status code: {response.status_code}")

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