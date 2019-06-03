from django import forms
import logging
from pytz import common_timezones

from woeip.apps.air_quality import models

logger = logging.getLogger(__name__)

# class DustrakSessionForm(forms.ModelForm):
#     air_quality = forms.FileField()
#     gps = forms.FileField()
#     timezone = forms.ChoiceField(choices=[(x, x) for x in common_timezones], initial='America/Los_Angeles')

#     class Meta():
#         model = models.Session
#         fields = ('collected_by', 'date_collected', 'route', 'air_quality', 'gps', 'timezone')


class UploadForm(forms.ModelForm):
    
    class Meta:
        model = models.UploadedFile
        fields = ('file',)
