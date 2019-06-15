from django import forms
from pytz import common_timezones

from woeip.apps.air_quality import models


# TODO: Document the name of SessionData Form is changed to Upload Field
# It seems like a more consistent naming conventio
class UploadForm(forms.ModelForm):
    """Both an air quality and a gps file are required for initial upload of data"""
    class Meta():
        model = models.SessionData
        fields = ('sensor_file', 'gps_file')

    def __init__(self, *args, **kwargs):
        """Zurb Foundation classes expand the area of the input fields,
        facilitating simple drag-and-drop functionality"""
        super(UploadForm, self).__init__(*args, **kwargs)
        for field in ['sensor_file', 'gps_file']:
            self.fields[field].widget.attrs.update({
                'class': 'callout primary large text-center'
                })


# TODO: This form does not link to models. This is because the fields are split between models.
# My intention is to manually save the datum from each field to the correct model
# TODO: The start day and time are currently one field in the form. However, it may be better
# to split into two separate fields
class ConfirmForm(forms.Form):
    """Users confirm that the automatically genderated information """
    start_datetime = forms.DateTimeField(label="Start day and time", input_formats=["%d %b %Y %H:%M:%S %Z"])
    timezone = forms.ChoiceField(label="Timezone", choices=[(x, x) for x in common_timezones])
    # TODO: Document that registered users are recognized as possible choices, in the field
    collected_by = forms.ModelChoiceField(label="Collected by", queryset=models.User.objects.all())
    device_name = forms.CharField(label="Device name")
    # TODO: Additional fields may be added, based on need
