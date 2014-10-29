#
# Generate Steam user information referring to games he recently played and owned.
#

my_steam_id = 76561198039618528

import getInfoFromSteam

def generate_game_info(app_id):
    app_id = str(app_id)
    res = getInfoFromSteam.get_game_details(app_id)
    print res
    return res

def generate_user_info(steam_id):
    owned_games = getInfoFromSteam.get_owned_games(steam_id)
    print owned_games
    app_id_list = []
    for i in owned_games:
        app_id_list.append(i['appid'])
    game_info_list = []
    print app_id_list
    for app_id in app_id_list:
        game_info = generate_game_info(app_id)
        if game_info == None: 
            print "NA"
            continue
        game_info_list.append(app_id)
        game_info_list.append(generate_game_info(app_id))
    #print game_info_list

if __name__ == "__main__":
    generate_user_info(my_steam_id)
