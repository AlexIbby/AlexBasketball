from xml.etree import ElementTree as ET


# The functions here assist in parsing the Yahoo API Endpoints Responses, largely in XML. 




# Relevant End Point: https://fantasysports.yahooapis.com/fantasy/v2/users;use_login=1/games;game_keys=nba.2023/leagues/teams
def extract_fantasy_info(root):
    ns = {'ns0': 'http://fantasysports.yahooapis.com/fantasy/v2/base.rng'}
    extracted_info = {}
    user = root.find('.//ns0:user', ns)
    
    # Extract the yahoo_user_id (guid)
    extracted_info['yahoo_user_id'] = user.find('.//ns0:guid', ns).text
    
    for game in user.findall('.//ns0:game', ns):
        if game.find('.//ns0:code', ns).text == 'nba':
            league = game.find('.//ns0:league', ns)
            extracted_info['league_key'] = league.find('.//ns0:league_key', ns).text
            extracted_info['league_id'] = league.find('.//ns0:league_id', ns).text
            
            team = league.find('.//ns0:team', ns)
            extracted_info['team_key'] = team.find('.//ns0:team_key', ns).text
            extracted_info['team_id'] = team.find('.//ns0:team_id', ns).text
            extracted_info['team_name'] = team.find('.//ns0:name', ns).text
            extracted_info['team_logo_url'] = team.find('.//ns0:team_logo//ns0:url', ns).text
            
            manager = team.find('.//ns0:manager', ns)
            extracted_info['manager_nickname'] = manager.find('.//ns0:nickname', ns).text
            
            break
    return extracted_info


#Parse XML 

def parse_yahoo_response_to_xml(response_content):
    return ET.fromstring(response_content)