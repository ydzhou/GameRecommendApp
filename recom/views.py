from django.shortcuts import render, get_object_or_404, redirect
from recom.models import UserSteamIDForm
import recommender as Recom
import getInfoFromSteam as Info

TEST = True

def recompage(request):
    if request.method == 'GET':
        return render(request, 'recom/steamID.html')

def submit(request):
    if request.method == 'POST':
        form = UserSteamIDForm(request.POST)
        if form.is_valid():
            posted_data = form.cleaned_data
            user_steamid = posted_data['steamID']
            if len(user_steamid)!=17 or user_steamid.isdigit() == False:
                return render(request, 'recom/submit.html', {'success': False})
            Recom.generate_recommended_game_info_threaded(user_steamid)
            return render(request, 'recom/submit.html', {'success': True})
        return render(request, 'recom/submit.html', {'success': False})
        
def result(request):
    if request.method == 'GET':
        res = Recom.get_recommended_game_info()
        success = res[0]
        if success == 0:
            return render(request, 'recom/submit.html', {'success': True})
        elif success == -1:
            return render(request, 'recom/submit.html', {'success': False})
        recom_apps = res[1]
        #recom_apps = [{'name':'YellowStar', 'url':'http://store.steampowered.com/app/65980', 'img':'http://cdn.akamai.steamstatic.com/steam/apps/65980/header.jpg?t=1414514300', 'descrip':"dafasdfasf afsdfasdf fasdfasfadsf a ads fadfa dadfafasdfasfasfasdfd fsadfasdfasf fadsf asdf asdf asf adsfads af adsfadsfadsfa asdf asda"}, {'name':'YellowStar', 'url':'http://store.steampowered.com/app/65980', 'img':'http://cdn.akamai.steamstatic.com/steam/apps/65980/header.jpg?t=1414514300', 'descrip':"dafasdfasf afsdfasdf fasdfasfadsf a ads fadfa dadfafasdfasfasfasdfd fsadfasdfasf fadsf asdf asdf asf adsfads af adsfadsfadsfa asdf asda"}]
        if recom_apps == []:
            return render(request, 'recom/submit.html', {'success': False})
        content = {
            'recom_apps' : recom_apps
        }
        return render(request, 'recom/recommend.html', content)