from sklearn import svm
from sklearn.naive_bayes import GaussianNB

from operator import itemgetter
import generateUserInfo as G
import getInfoFromSteam
import math

my_steam_id = 76561198039618528
#my_steam_id = 76561198060149220
# HarderQ 76561198039618528

def recommend_games(steam_id):
    recom_apps = []
    
    [xt, yt] = generate_IR_training_data(steam_id)
    
    if xt == None or yt == None:
        return recom_apps
    
    #clf = svm.SVR()
    #clf.fit(xt, yt)
    #yp_t = clf.predict(xt)
    
    recom = GaussianNB()
    recom.fit(xt, yt)
    #yp_t = recom.predict(xt)
    #print yp_t
    
    #err = 0
    #for i in range(len(yt)):
    #    err += abs(yt[i] - yp_t[i])
    #print err/11

    owned_apps = G.get_all_games(steam_id)
    trending_apps = get_trending_games_played_by_friends(steam_id, 40)
    if trending_apps == None:
        return recom_apps # None
    
    app_predict = []

    for app_id in trending_apps:
        if app_id in owned_apps:
            continue
        app_details = G.get_app_details(app_id)
        if app_details == None: continue
        shared_genres = 0
        xp = []
        for i in range(G.get_genres_index("", 2)):
            xp.append(0)
        for app_genres in app_details:
            genres_id = app_genres['id']
            pos = G.get_genres_index(genres_id, 0)
            if (pos)>=0:
                shared_genres = 1
                xp[pos] = 1
        if shared_genres == 1:
            print xp
            yp = recom.predict(xp)
            print 'app yp: ', yp
            app_predict.append([app_id, yp])
            if yp == 1:
                if len(recom_apps)>=3:
                    return recom_apps
                if app_id not in recom_apps:
                    recom_apps.append(app_id)
    app_predict.sort(key=itemgetter(1), reverse=True)
    recom_apps = []
    i = 0
    for app in app_predict:
        if (i>=3): 
            break
        recom_apps.append(app[0])
    return recom_apps
    
def get_trending_games_played_by_friends(steam_id, num_of_friend):
    friends = G.get_friends(steam_id)
    if friends == None:
        return None
    all_apps = {}
    num = 0
    for f in friends:
        print 'collect info from friend', f
        single_user_apps = G.get_recently_played_games(f)
        if single_user_apps == None:
            continue
        for app in single_user_apps:
            app_id = app[0]
            playtime_2weeks = app[1]
            if app_id in all_apps:
                all_apps[app_id] += playtime_2weeks
            else:
                all_apps[app_id] = playtime_2weeks
        if num > num_of_friend:
            break
        else:
            num += 1
    sorted_all_apps = sorted(all_apps.items(), key=itemgetter(1), reverse=True)
    print sorted_all_apps
    res = [a[0] for a in sorted_all_apps]
    return res
    
def generate_IR_training_data(steam_id):
    xt = [] # input vector for training
    yt = [] # target vector for training

    steam_id = str(steam_id)
    app_info = G.get_user_info_genres_based(steam_id)
    if app_info == None:
        return [None, None]

    total_num_of_genres_ids = G.get_genres_index('', 2)
    
    owned_genres_bitvec_single = []
    
    # sum up playtime of all the apps with same genres pattern
    app_info_re = {}
    
    for app in app_info:
        app_id = app[0]
        app_detail = app[3]
        xt_app = []
        for i in range(total_num_of_genres_ids):
            xt_app.append(0)
        for app_genres in app_detail:
            genres_id = app_genres['id']
            pos = G.get_genres_index(genres_id, 1)
            if pos >= 0:
                xt_app[pos] = 1
                if (1<<pos) not in owned_genres_bitvec_single:
                    owned_genres_bitvec_single.append(1<<pos)
        genres_bitvec = listToBitVec(xt_app)
        genres_bitvec = str(genres_bitvec)
        if genres_bitvec in app_info_re:
            app_info_re[genres_bitvec][0] += app[1]
            app_info_re[genres_bitvec][1] += app[2]
        else:
            app_info_re[genres_bitvec] = [app[1], app[2]]
    
    # print app_info_re
    print owned_genres_bitvec_single
    
    max_playtime = 0
    max_playtime_2weeks = 0
    
    for genres_bitvec in app_info_re:
        max_playtime_2weeks = max(max_playtime_2weeks, app_info_re[genres_bitvec][0])
        max_playtime = max(max_playtime, app_info_re[genres_bitvec][1])
        xt_app = bitvecToList(int(genres_bitvec), total_num_of_genres_ids)
        xt.append(xt_app)
        
    if max_playtime == 0:
        return [None, None]

    for genres_bitvec in app_info_re:
        playtime_2weeks = float(app_info_re[genres_bitvec][0])
        playtime = float(app_info_re[genres_bitvec][1])
        playtime_n = playtime/max_playtime
        try:
            playtime_2weeks_n = playtime_2weeks/max_playtime_2weeks
        except:
            playtime_2weeks_n = 0
        pi = 3.1416
        yt_app = math.tanh(playtime_n*pi)/5*4 + 0.25
        yt_app *= math.tanh(playtime_2weeks_n*pi*2)/3 + 0.9
        if playtime != 0:
            if yt_app < (playtime_2weeks/playtime):
                yt_app = playtime_2weeks/playtime
        if yt_app > 1:
            yt_app = 1.0000
        yt.append(yt_app)
    
    # generate training vector for non-existed genres to balance the recommender regression
    for i in range(11):
        genres_bitvec = (1 << i)
        if genres_bitvec in owned_genres_bitvec_single:
            continue
        xt.append(bitvecToList(genres_bitvec, total_num_of_genres_ids))
        yt.append(0)
        
        
    # print xt
    # print yt
    
    return [xt, yt]
    
def listToBitVec(lst):
    if lst == [] or lst == None:
        return -1
    s = 0
    for i in lst:
        s = (s << 1) + i
    return s

def bitvecToList(bitvec, n):
    lst = []
    while bitvec > 0:
        lst.append(bitvec & 1)
        bitvec = bitvec >> 1
    for i in range(n - len(lst)):
        lst.append(0)
    lst.reverse()
    return lst

# Test Purpose
if __name__=="__main__":
    print recommend_games(my_steam_id)
    #print get_trending_games_played_by_friends(my_steam_id, 5)
    #print generate_IR_training_data(my_steam_id)