from sklearn import svm
from operator import itemgetter
import generateUserInfo
import getInfoFromSteam

my_steam_id = 76561198039618528

def recommend_games(steam_id):
    [xt, yt] = generateUserInfo.generate_IR_training_data(steam_id)
    
    clf = svm.SVR()
    clf.fit(xt, yt)
    
    recom_apps = []

    owned_apps = generateUserInfo.get_all_games(steam_id)
    trending_apps = get_trending_games_played_by_friends(steam_id)
    if trending_apps == None:
        return None

    for app_id in trending_apps:
        if app_id in owned_apps:
            continue
        app_details = generateUserInfo.get_app_details(app_id)
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
                if len(recom_apps)>=3:
                    return recom_apps
                if app_id not in recom_apps:
                    recom_apps.append(app_id)
    return recom_apps
    
def get_trending_games_played_by_friends(steam_id):
    friends = generateUserInfo.get_friends(steam_id)
    if friends == None:
        return None
    all_apps = {}
    for f in friends:
        print 'collect info from friend', f
        single_user_apps = generateUserInfo.get_recently_played_games(f)
        if single_user_apps == None:
            continue
        for app in single_user_apps:
            app_id = app[0]
            playtime_2weeks = app[1]
            if app_id in all_apps:
                all_apps[app_id] += playtime_2weeks
            else:
                all_apps[app_id] = playtime_2weeks
    sorted_all_apps = sorted(all_apps.items(), key=itemgetter(1), reverse=True)
    print sorted_all_apps
    res = [a[0] for a in sorted_all_apps]
    return res
        

if __name__=="__main__":
    print recommend_games(my_steam_id)
    #print get_trending_games_played_by_friends(my_steam_id, 5)
