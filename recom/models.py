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
        return self.appid
    
class User(models.Model):
    steam_id = models.CharField(max_length=17)
    #last_update = models.DateField(default=None)
    friend = models.ManyToManyField('self')
    #recommended_apps = models.ManyToManyField(App)
    def __unicode__(self):
        return self.steam_id
    
class UserOwnedGames(models.Model):
    user = models.ForeignKey(User)
    appid = models.CharField(max_length=20, default='')
    playtime = models.IntegerField(default=0)
    playtime_2weeks = models.IntegerField(default=0)