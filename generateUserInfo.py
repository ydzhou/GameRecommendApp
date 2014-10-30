#
# Generate Steam user's information referring to games he has recently played and owned.
#

my_steam_id = 76561198039618528

from operator import itemgetter
import json
import getInfoFromSteam
import os
import math

def get_user_info_genres_based(steam_id):
    # TODO: update user info via get_recently_played_game
    #       try to update playtime and inventory
    #       need time stamp to update playtime_2weeks
    steam_id = str(steam_id)
    # filename = './data/user_info.json'
    # if os.path.isfile(filename):
    #     with open(filename, 'r') as f:
    #         for line in f:
    #             try:
    #                 user_info = json.loads(line.strip())
    #             except:
    #                 continue
    #             if steam_id in user_info:
    #                 return user_info[steam_id]
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
        app_detail = get_app_details(app_id)
        if app_detail == None:
            continue
        app_info = [app_id, playtime_2weeks, playtime, app_detail]
        user_info.append(app_info)
        max_playtime = max(max_playtime, playtime)
    user_info.sort(key=itemgetter(2))
    user_info_t = []
    for u in user_info:
        if float(u[2])/max_playtime > 0.1 or u[1] > 0:
            user_info_t.append(u)
    #with open(filename, 'a') as f:
    #    f.write("\n")
    #    json.dump({steam_id : user_info}, f)
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
    total_num_of_genres_ids = get_genres_index('', 2)
    
    for app in app_info:
        app_id = app[0]
        app_detail = app[3]
        xt_app = []
        for i in range(total_num_of_genres_ids):
            xt_app.append(0)
        for app_genres in app_detail:
            genres_id = app_genres['id']
            pos = get_genres_index(genres_id, 1)
            if pos >= 0:
                xt_app[pos] = 1
        xt.append(xt_app)
        max_playtime = max(max_playtime, app[2])
        max_playtime_2weeks = max(max_playtime_2weeks, app[1])

    for app in app_info:
        playtime_n = float(app[2])/max_playtime
        playtime_2weeks_n = float(app[1])/max_playtime_2weeks
        pi = 3.1416
        yt_app = math.tanh(playtime_n*pi)
        yt_app *= math.tanh(playtime_2weeks_n*pi)/2 + 0.5
        if yt_app < (float(app[1])/app[2]):
            yt_app = float(app[1])/app[2]
        yt.append(yt_app)
        
    #print xt
    #print yt
    
    return [xt, yt]

def get_friends(steam_id):
    friend_info = getInfoFromSteam.get_friend_list(steam_id)
    friends = []
    for f in friend_info:
        friends.append(f['steamid'])
    return friends

def get_recently_played_games(steam_id):
    # app_id, playtime_2weeks
    app_list = getInfoFromSteam.get_recently_played_games(steam_id)
    if app_list == None:
        return None
    res = []
    for app in app_list:
        if app['playtime_forever']>=10 or float(app['playtime_2weeks'])/app['playtime_forever']>=0.5:
            res.append([app['appid'], app['playtime_2weeks']])
    return res

def get_all_games(steam_id):
    app_list = getInfoFromSteam.get_owned_games(steam_id)
    res = []
    for app in app_list:
        res.append(app['appid'])
    return res

def get_app_details(app_id):
    # TODO: add game tags to game_detail
    app_id = str(app_id)
    filename = './data/app_info.json'
    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            for line in f:
                try:
                    app_detail = json.loads(line.strip())
                except:
                    continue
                if app_id in app_detail:
                    return app_detail[app_id]
    app_detail = getInfoFromSteam.get_game_details(app_id)
    app_detail = {app_id:app_detail}
    with open(filename, 'a') as f:
        f.write("\n")
        json.dump(app_detail, f)
    return app_detail[app_id]

def get_genres_index(genres_id, flag):
    with open('./data/genres_id.json', 'r') as f:
        genres_ids = json.loads(f.read())
    if flag == 2:
        return len(genres_ids)
    if genres_id not in genres_ids:
        return -1
    return genres_ids[genres_id]

if __name__ == "__main__":
    generate_IR_training_data(my_steam_id)
    #get_recently_played_games(my_steam_id)
    #print get_user_info_genres_based(my_steam_id)
    #print get_app_details('550')
