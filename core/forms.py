from django.forms import ModelForm
from . import models


class SyncFeedForm(ModelForm):
    
    class Meta:
        model = models.SyncFeed
        fields = ['email']