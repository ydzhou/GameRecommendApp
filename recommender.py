from sklearn import svm
import generateUserInfo
import getInfoFromSteam

my_steam_id = 76561198039618528

def recommend_game(steam_id):
    #[xt, yt] = generateUserInfo.generate_IR_training_data(steam_id)
    xt = [[1, 1, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 1]]
    yt = [0.2230981388768579, 0.2888380878035431, 0.9800030641159568, 0.4963324857514975, 0.49813606544598416]
    
    clf = svm.SVR()
    clf.fit(xt, yt)
    
    recom_apps = []

    owned_apps = generateUserInfo.get_all_games(steam_id)
    friends = generateUserInfo.get_friends(steam_id)
    for f in friends:
        print 'recommend game from friend: ', f
        apps = generateUserInfo.get_recently_played_games(f)
        if apps == None:
            continue
        for app_id in apps:
            if app_id in owned_apps:
                continue
            app_details = getInfoFromSteam.get_game_details(app_id)
            shared_genres = 0
            xp = []
            for i in range(generateUserInfo.get_genres_index("", 2)):
                xp.append(0)
            for app_genres in app_details:
                genres_id = app_genres['id']
                pos = generateUserInfo.get_genres_index(genres_id, 0)
                if (pos)>=0:
                    shared_genres = 1
                    xp[pos] = 1
            if shared_genres == 1:
                print xp
                yp = clf.predict(xp)
                print 'app yp: ', yp
                if yp > 0.5:
                    if app_id not in recom_apps:
                        recom_apps.append(app_id)
    return recom_apps
                    

if __name__=="__main__":
    print recommend_game(my_steam_id)
