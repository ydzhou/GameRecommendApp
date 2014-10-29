#
# Get User Information through Steam API
# Steam API Key: C1A6C90A09B7FCE900DD0B7F2EFAA324

import urllib2
import json

steam_API_key = 'C1A6C90A09B7FCE900DD0B7F2EFAA324'
player_base_url = 'http://api.steampowered.com/IPlayerService/'
app_base_url = 'http://api.steampowered.com/ISteamUserStats/'
my_steam_id = 76561198039618528

# Return Format: {'game_count': x, 'games': [{'playtime_forever': y, 'appid': z}, {...}]}
def get_owned_games(steam_id):
    steam_id = str(steam_id)
    url = player_base_url + 'GetOwnedGames/v0001/?key=' + steam_API_key + '&steamid=' + steam_id + '&format=json'
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    the_page = response.read()
    res = json.loads(the_page)
    return res['response']['games']

def get_recently_played_games(steam_id):
    steam_id = str(steam_id)
    url = player_base_url + 'GetRecentlyPlayedGames/v0001/?key=' + steam_API_key + '&steamid=' + steam_id + '&format=json'
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    the_page = response.read()
    res = json.loads(the_page)
    return res['response']['games']
    
def get_schema_for_game(app_id):
    app_id = str(app_id)
    url = app_base_url + 'GetSchemaForGame/v2/?key=' + steam_API_key + '&appid=' + app_id
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    the_page = response.read()
    res = json.loads(the_page)
    return res

def get_game_tags(app_id):
    app_id = str(app_id)
    url = 'http://store.steampowered.com/app/' + app_id
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    the_page = response.read()
    app_tag_pos = the_page.find('tagid') - 3
    print app_tag_pos
    if (app_tag_pos<0): return None
    app_tag_raw = ''
    while the_page[app_tag_pos] != ']':
        app_tag_raw += the_page[app_tag_pos]
        app_tag_pos += 1
    app_tag_raw += ']'
    res = json.loads(app_tag_raw)
    print 'done'
    return res

def get_game_details(app_id):
    app_id = str(app_id)
    url = 'http://store.steampowered.com/api/appdetails/?appids=' + app_id
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    the_page = response.read() 
    res = json.loads(the_page)
    if res[app_id]['success'] == False:
        return None
    return [
        res[app_id]['data']['name'],
        res[app_id]['data']['genres']
    ]

if __name__ == "__main__":
        res = get_recently_played_games(my_steam_id)
        recent_played_games = res
        app_id = recent_played_games[0]['appid']
        #game_info = get_schema_for_game(app_id)
        get_game_details(app_id)
