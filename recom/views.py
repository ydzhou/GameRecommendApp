from django.shortcuts import render, get_object_or_404, redirect
from recom.models import UserSteamIDForm
import recommender as Recom
import getInfoFromSteam as Info

TEST = True

def recompage(request):
    if request.method == 'GET':
        return render(request, 'recom/index.html')
        
def submit(request):
    if request.method == 'POST':
        form = UserSteamIDForm(request.POST)
        if form.is_valid():
            posted_data = form.cleaned_data
            user_steamid = posted_data['steamID']
            if len(user_steamid)!=17 or user_steamid.isdigit() == False:
                lenErr = (len(user_steamid)!=17)
                digErr = user_steamid.isdigit()
                content = {
                    'lenErr': lenErr,
                    'digErr': digErr
                }
                return render(request, 'recom/error.html', content)
            recom_apps = Recom.get_recommended_games(user_steamid)
            
            #recom_apps = [{'name':'YellowStar', 'url':'http://store.steampowered.com/app/65980', 'img':'http://cdn.akamai.steamstatic.com/steam/apps/65980/header.jpg?t=1414514300', 'descrip':"dafasdfasf afsdfasdf fasdfasfadsf a ads fadfa dadfafasdfasfasfasdfd fsadfasdfasf fadsf asdf asdf asf adsfads af adsfadsfadsfa asdf asda"}]
            
            content = {
                'recom_apps' : recom_apps
            }
            
            return render(request, 'recom/recommend.html', content)
        return render(request, 'recom/error.html')