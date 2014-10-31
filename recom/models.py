from django.db import models
from django import forms

class UserSteamIDForm(forms.Form):
    steamID = forms.CharField(max_length=20)