from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    yahoo_user_id = db.Column(db.String(256), unique=True)  # Yahoo User ID
    access_token = db.Column(db.String(2048))
    expires_at = db.Column(db.Integer)
    expires_in = db.Column(db.Integer)
    refresh_token = db.Column(db.String(256))
    token_type = db.Column(db.String(64))
    league_key = db.Column(db.String(256))  
    league_id = db.Column(db.String(256))   
    team_key = db.Column(db.String(256))    
    team_id = db.Column(db.String(256))     
    team_name = db.Column(db.String(256))   
    team_logo_url = db.Column(db.String(512)) 
    manager_nickname = db.Column(db.String(256))  

    def __init__(self, yahoo_user_id, access_token, expires_at, expires_in, refresh_token, token_type, 
                 league_key, league_id, team_key, team_id, team_name, team_logo_url, manager_nickname):
        self.yahoo_user_id = yahoo_user_id
        self.access_token = access_token
        self.expires_at = expires_at
        self.expires_in = expires_in
        self.refresh_token = refresh_token
        self.token_type = token_type
        self.league_key = league_key
        self.league_id = league_id
        self.team_key = team_key
        self.team_id = team_id
        self.team_name = team_name
        self.team_logo_url = team_logo_url
        self.manager_nickname = manager_nickname