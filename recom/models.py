from django.db import models
from django import forms

class UserSteamIDForm(forms.Form):
    steamID = forms.CharField(max_length=20)

# Database to store app and user information

class App(models.Model):
    appid = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    descript = models.TextField()
    img = models.TextField()
    score = models.IntegerField()
    genres = models.CharField(max_length=200, default='[]')
    publisher = models.CharField(max_length=100, default='NA')
    release_date = models.CharField(max_length=50, default='NA')
    #categories = models.TextField(default='NA')
    url = models.TextField(default='NA')
    def __unicode__(self):
        return self.app_id
    
class User(models.Model):
    steam_id = models.CharField(max_length=17)
    last_update = models.DateField()
    def __unicode__(self):
        return self.steam_id
    
class UserOwnedGames(models.Model):
    user = models.ForeignKey(User)
    app = models.ManyToManyField(App)
    playtime = models.IntegerField()
    playtime_2weeks = models.IntegerField()