#
# Generate Steam user information referring to games he recently played and owned.
#

my_steam_id = 76561198039618528

from operator import itemgetter
import json
import getInfoFromSteam
import datetime
import os
import math

def get_user_info_tag_based(steam_id):
    steam_id = str(steam_id)
    #if os.path.isfile(steam_id + '.txt'):
    #    f = open(steam_id + '.txt', 'r')
    #    user_info = json.loads(f.read())
    #    return user_info[steam_id]
    owned_games = getInfoFromSteam.get_owned_games(steam_id)
    user_info = []
    for app in owned_games:
        app_id = app['appid']
        playtime = app['playtime_forever']
        if 'playtime_2weeks' in app:
            playtime_2weeks = app['playtime_2weeks']
        else:
            playtime_2weeks = 0
        app_tags = getInfoFromSteam.get_game_tags(app_id)
        if app_tags == None:
            continue
        app_info = [app_id, playtime_2weeks, playtime, app_tags]
        user_info.append(app_info)
    user_info.sort(key=itemgetter(2))
    
    print(user_info[len(user_info)-10 : len(user_info)])
    
    with open(steam_id + '.txt', 'w') as f:
        json.dump({steam_id : user_info}, f)
    return user_info

def get_user_info_genres_based(steam_id):
    steam_id = str(steam_id)
    #if os.path.isfile(steam_id + '.txt'):
    #    f = open(steam_id + '.txt', 'r')
    #    user_info = json.loads(f.read())
    #    return user_info[steam_id]
    owned_games = getInfoFromSteam.get_owned_games(steam_id)
    user_info = []
    max_playtime = 0
    for app in owned_games:
        app_id = app['appid']
        playtime = app['playtime_forever']
        if 'playtime_2weeks' in app:
            playtime_2weeks = app['playtime_2weeks']
        else:
            playtime_2weeks = 0
        app_detail = getInfoFromSteam.get_game_details(app_id)
        if app_detail == None:
            continue
        app_info = [app_id, playtime_2weeks, playtime, app_detail]
        user_info.append(app_info)
        max_playtime = max(max_playtime, playtime)
    user_info.sort(key=itemgetter(2))
    user_info_t = []
    for u in user_info:
        if float(u[2])/max_playtime > 0.1:
            user_info_t.append(u)
    with open(steam_id + '.txt', 'w') as f:
        json.dump({steam_id : user_info}, f)
    return user_info_t


# input vector: a bit-map for genre
# output vector: playtime-based metric scaled into [0, 1]
def generate_IR_training_data(steam_id):
    xt = [] # input
    yt = [] # target

    steam_id = str(steam_id)
    app_info = get_user_info_genres_based(steam_id)
    max_playtime = 0
    max_playtime_2weeks = 0
    total_num_genres_ids = 0

    for app in app_info:
        app_id = app[0]
        app_detail = app[3]
        xt_app = []
        for i in range(6):
            xt_app.append(0)
        for app_genres in app_detail:
            genres_id = app_genres['id']
            pos = get_genres_index(genres_id, 1)
            xt_app[pos] = 1
        xt.append(xt_app)
        max_playtime = max(max_playtime, app[2])
        max_playtime_2weeks = max(max_playtime_2weeks, app[1])
    
    total_num_genres_ids = get_genres_index(genres_id, 2)

    for app in app_info:
        playtime_n = float(app[2])/max_playtime
        playtime_2weeks_n = float(app[1])/max_playtime_2weeks
        pi = 3.1416
        yt_app = math.tanh(playtime_n*pi)
        yt_app *= math.tanh(playtime_2weeks_n*pi)/2 + 0.5
        yt.append(yt_app) 

    return [xt, yt]

def get_friends(steam_id):
    friend_info = getInfoFromSteam.get_friend_list(steam_id)
    friends = []
    for f in friend_info:
        friends.append(f['steamid'])
    return friends

def get_recently_played_games(steam_id):
    app_list = getInfoFromSteam.get_recently_played_games(steam_id)
    if app_list == None:
        return None
    res = []
    for app in app_list:
        if app['playtime_forever']<10:
            continue
        res.append(app['appid'])
    return res

def get_all_games(steam_id):
    app_list = getInfoFromSteam.get_owned_games(steam_id)
    res = []
    for app in app_list:
        res.append(app['appid'])
    return res

def get_genres_index(genres_id, flag):
    f = open('genres_id.txt', 'r')
    genres_ids = json.loads(f.read())
    f.close()
    if flag == 2:
        return len(genres_ids)
    if flag == 0:
        if genres_id in genres_ids: return genres_ids[genres_id]
        else: return -1
    if genres_id in genres_ids:
        return genres_ids[genres_id]
    genres_ids[genres_id] = len(genres_ids)
    with open('genres_id.txt', 'w') as f:
        json.dump(genres_ids, f)
    return genres_ids[genres_id]

if __name__ == "__main__":
    #generate_IR_training_data(my_steam_id)
    #get_recently_played_games(my_steam_id)
    print get_genres_index('28', 1)
    print get_genres_index('28', 0)
    print get_genres_index('28', 2)
