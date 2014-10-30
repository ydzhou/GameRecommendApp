#
# Get User Information through Steam API
# Steam API Key: C1A6C90A09B7FCE900DD0B7F2EFAA324

import urllib2
import json
import requests
import datetime

steam_API_key = 'C1A6C90A09B7FCE900DD0B7F2EFAA324'
base_url = 'http://api.steampowered.com/'
my_steam_id = 76561198039618528

# Return Format: {'game_count': x, 'games': [{'playtime_forever': y, 'appid': z}, {...}]}
def get_owned_games(steam_id):
    steam_id = str(steam_id)
    url = base_url + 'IPlayerService/GetOwnedGames/v0001/?key=' + steam_API_key + '&steamid=' + steam_id + '&format=json'
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    the_page = response.read()
    res = json.loads(the_page)
    return res['response']['games']

def get_recently_played_games(steam_id):
    steam_id = str(steam_id)
    url = base_url + 'IPlayerService/GetRecentlyPlayedGames/v0001/?key=' + steam_API_key + '&steamid=' + steam_id + '&format=json'
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    the_page = response.read()
    res = json.loads(the_page)
    if 'games' not in res['response']:
        return None
    return res['response']['games']

def get_friend_list(steam_id):
    # un-functionable if user sets its profile to not be public
    steam_id = str(steam_id)
    url = base_url + 'ISteamUser/GetFriendList/v0001/?key=' + steam_API_key + '&steamid=' + steam_id + '&relationship=friend'
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    the_page = response.read()
    res = json.loads(the_page)
    try:
        return res['friendslist']['friends']
    except:
        return None

# Use Steam HTTP API to retrieve game details
def get_game_details(app_id):
    app_id = str(app_id)
    url = 'http://store.steampowered.com/api/appdetails/?appids=' + app_id
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    the_page = response.read() 
    res = json.loads(the_page)
    if res[app_id]['success'] == False:
        return None
    else:
        return res[app_id]['data']['genres']

# A crawler to fetch game tags
def get_game_tags(app_id):
    tstart = datetime.datetime.now()
    app_id = str(app_id)
    url = 'http://store.steampowered.com/app/' + app_id
    session = requests.session()
    the_page = session.get(url).text
    if ('<form action="http://store.steampowered.com/agecheck/app/%s/"' % app_id) in the_page:
        post_data = {
                'snr': '1_agecheck_agecheck_age-gate',
                'ageDay': 1,
                'ageMonth': 'January',
                'ageYear': '1990'
                }
        the_page = session.post('http://store.steampowered.com/agecheck/app/%s/' % app_id, post_data).text
    tend = datetime.datetime.now()
    print tend - tstart
    start_tag = 'InitAppTagModal( %s,' % app_id
    end_tag = '],'
    start_index = the_page.find(start_tag) + len(start_tag)
    if start_index - len(start_tag) < 0:
        return None
    end_index = the_page.find(end_tag, start_index) + len(end_tag) - 1
    tags = json.loads(the_page[start_index:end_index])
    res = []
    for i in range(4):
        res.append({tags[i]['tagid']: tags[i]['count']})
    return res


if __name__ == "__main__":
    #get_friend_list(my_steam_id)
    get_recently_played_games(76561198068784324)
