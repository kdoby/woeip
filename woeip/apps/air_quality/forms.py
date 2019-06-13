from django import forms

from woeip.apps.air_quality import models


class SessionDataForm(forms.ModelForm):
    """Both an air quality and a gps file are required for initial upload of data"""
    class Meta():
        model = models.SessionData
        fields = ('upload', 'upload_gps')

    def __init__(self, *args, **kwargs):
        """Zurb Foundation classes expand the area of the input fields,
        facilitating simple drag-and-drop functionality"""
        super(SessionDataForm, self).__init__(*args, **kwargs)
        self.fields['upload'].widget.attrs.update({
            'class': 'callout primary large text-center'
            })
        self.fields['upload_gps'].widget.attrs.update({
            'class': 'callout primary large text-center'
            })

# Document that it doesn't link to a model because the values are split between two models: session and sessionData
class SessionForm(forms.Form):
    start_datetime = forms.DateTimeField()
    collected_by = forms.
    class Meta():
        # Start datetime
        # Device
        # Collected by
        model = models.Session
        fields = ()