from django.shortcuts import render, get_object_or_404, redirect
from recom.models import UserSteamIDForm
import recommender as Recom

TEST = True

def recompage(request):
    if request.method == 'GET':
        return render(request, 'recom/index.html')
        
def submit(request):
    if request.method == 'POST':
        form = UserSteamIDForm(request.POST)
        #if form.is_valid():
        posted_data = form
        user_steamid = posted_data['steamID']
            #if len(user_steamid)!=16 or user_steamid.digits == False:
            #    return render(request, 'recom/index.html')
            #recom_apps = Recom.recommend_games(user_steamid)
            
        content = {
            'recom_apps' : ['1111', '222', '333']
        }
            
        return render(request, 'recom/recommend.html', content)