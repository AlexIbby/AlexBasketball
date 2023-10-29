from models import User, db


def update_or_create_user(token, extracted_user_info):
    # Replace the query logic based on how you're checking for existing users
    existing_user = User.query.filter_by(access_token=token.get('access_token')).first()

    if existing_user:
        # Update existing user's fields
        existing_user.access_token = token.get('access_token')
        existing_user.expires_at = token.get('expires_at')
        existing_user.expires_in = token.get('expires_in')
        existing_user.refresh_token = token.get('refresh_token')
        existing_user.token_type = token.get('token_type')

        #Adding in extracted info
        existing_user.yahoo_user_id = extracted_user_info.get('yahoo_user_id')
        existing_user.league_key = extracted_user_info.get('league_key')
        existing_user.league_id = extracted_user_info.get('league_id')
        existing_user.team_key = extracted_user_info.get('team_key')
        existing_user.team_id = extracted_user_info.get('team_id')
        existing_user.team_name = extracted_user_info.get('team_name')
        existing_user.team_logo_url = extracted_user_info.get('team_logo_url')
        existing_user.manager_nickname = extracted_user_info.get('manager_nickname')

    else:
        # Create new user
        new_user = User(
            access_token=token.get('access_token'),
            expires_at=token.get('expires_at'),
            expires_in=token.get('expires_in'),
            refresh_token=token.get('refresh_token'),
            token_type=token.get('token_type'),

            #extracted info
            yahoo_user_id=extracted_user_info.get('yahoo_user_id'),
            league_key=extracted_user_info.get('league_key'),
            league_id=extracted_user_info.get('league_id'),
            team_key=extracted_user_info.get('team_key'),
            team_id=extracted_user_info.get('team_id'),
            team_name=extracted_user_info.get('team_name'),
            team_logo_url=extracted_user_info.get('team_logo_url'),
            manager_nickname=extracted_user_info.get('manager_nickname')
        )

        db.session.add(new_user)

        existing_user = new_user  # so that we can return it

    db.session.commit()

    return existing_user  # Return the user, whether new or updated
