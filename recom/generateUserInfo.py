#
# Generate Steam user's information referring to games he has recently played and owned.
#
from operator import itemgetter
import json
from recom import getInfoFromSteam
import os
import math
import re
from recom.models import UserOwnedGames, User, App

my_steam_id = 76561198039618528

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
    
    if max_playtime == 0:
        return None
    
    user_info.sort(key=itemgetter(2))
    user_info_t = user_info
    #for u in user_info:
    #    if float(u[2])/max_playtime >= 0 or u[1] > 0:
    #        user_info_t.append(u)
    #with open(filename, 'a') as f:
    #    f.write("\n")
    #    json.dump({steam_id : user_info}, f)
    return user_info_t

def get_friends(steam_id):
    friend_info = getInfoFromSteam.get_friend_list(steam_id)
    friends = []
    for f in friend_info:
        friends.append(f['steamid'])
    return friends

def get_friends_database_based(steam_id):
    master_user = User.objects.get(steam_id__exact=steam_id)
    friend_info_in_db = master_user.friend.all()
    friends = []
    if not friend_info_in_db:
        print "Get friends via Steam Web API\n"
        friend_info = getInfoFromSteam.get_friend_list(steam_id)
        if friends == None:
            return None
        for f in friend_info:
            new_user = User(
                steam_id=f['steamid'],
            )
            new_user.save()
            master_user.friend.add(new_user)
            friends.append(f['steamid'])
    else:
        for f in friend_info_in_db:
            friends.append(f.steam_id)
    return friends

def get_recently_played_games(steam_id):
    # app_id, playtime_2weeks
    app_list = get_owned_game_database_based(steam_id)
    if app_list == None:
        return None
    res = []
    for app in app_list:
        try:
            playtime_2weeks = app['playtime_2weeks']
        except:
            playtime_2weeks = 0
        if app['playtime_forever'] > 0:
            if playtime_2weeks>=10 or float(playtime_2weeks)/app['playtime_forever']>=0.5:
                res.append([app['appid'], playtime_2weeks])
    return res
    # non-db method
    # app_list = getInfoFromSteam.get_recently_played_games(steam_id)
    # if app_list==None:
    #     return None
    # res = []
    # for app in app_list:
    #     if app['playtime_forever']>=10 or float(app['playtime_2weeks'])/app['playtime_forever']>=0.5:
    #         res.append([app['appid'], app['playtime_2weeks']])
    # return res

def get_all_games(steam_id):
    app_list = get_owned_game_database_based(steam_id)
    res = []
    for app in app_list:
        res.append(app['appid'])
    return res
    # non-db method
    # app_list = getInfoFromSteam.get_owned_games(steam_id)
    # res = []
    # for app in app_list:
    #     res.append(app['appid'])
    # return res

def get_owned_game_database_based(steam_id):
    user_in_db = User.objects.get(steam_id__exact=steam_id)
    userownedgame_in_db = UserOwnedGames.objects.all().filter(user=user_in_db)
    app_list = []
    if not userownedgame_in_db:
        print "Fetch owned games via Steam Web API\n"
        app_list = getInfoFromSteam.get_owned_games(steam_id)
        for app in app_list:
            try:
                playtime_2weeks = app['playtime_2weeks']
            except:
                playtime_2weeks = 0
            new_userownedgame = UserOwnedGames(
                user = user_in_db,
                appid = app['appid'],
                playtime = app['playtime_forever'],
                playtime_2weeks = playtime_2weeks
            )
            new_userownedgame.save()
    else:
        for uog in userownedgame_in_db:
            app = {}
            app['appid'] = uog.appid
            app['playtime_forever'] = uog.playtime
            if uog.playtime_2weeks > 0:
                app['playtime_2weeks'] = uog.playtime_2weeks
            app_list.append(app)
    return app_list

# preferred one to manage app information
def get_app_info_database_based(app_ids):
    # TODO: add game tags to game_detail
    apps_info = []
    for app_id in app_ids:
        try:
            app_info_in_db = App.objects.get(appid__exact=app_id)
            app_info = {}
            app_info['app_id'] = app_info_in_db.appid
            app_info['name'] = app_info_in_db.name
            app_info['descript'] = app_info_in_db.descript
            app_info['img'] = app_info_in_db.img
            app_info['publisher'] = app_info_in_db.publisher
            app_info['release_date'] = app_info_in_db.release_date
            app_info['score'] = app_info_in_db.score
            app_info['url'] = app_info_in_db.url
        except:
            app_info = getInfoFromSteam.get_game_info(app_id)
            new_app = App(
                appid=app_info['app_id'],
                name=app_info['name'],
                descript=app_info['descript'],
                img=app_info['img'],
                publisher=app_info['publisher'],
                release_date=app_info['release_date'],
                score=app_info['score'],
                url=app_info['url']
            )
            new_app.save()
        apps_info.append(app_info)
    return apps_info
    
# get app genres info from json file    
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
