import logging
# Settings to access static media
import os
import urllib

import pandas
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
# from settings import PUBLIC_ROOT
from django.utils.encoding import force_text
from django.views import View

from .dustrak import load_dustrak
from .forms import ConfirmForm, UploadForm
from .models import SessionData, User

logger = logging.getLogger(__name__)


class Upload(LoginRequiredMixin, View):
    def get(self, request):
        """Present file upload form to user"""
        return render(self.request, 'air_quality/upload.html', {
            'form': UploadForm
        })

    def post(self, request):
        """Save files to SessionData table"""
        files = self.request.FILES
        form = UploadForm(self.request.POST, files)
        if form.is_valid():
            session_data = form.save()
            messages.add_message(self.request, messages.SUCCESS, 'Files successfully uploaded')
            path = redirect('confirm', session_data_id=session_data.id)
        else:
            messages.add_message(self.request, messages.ERROR, 'File upload error')
            path = render(self.request, 'air_quality/upload.html', {
                'form': UploadForm
            })
        return path


# TODO: Add logic to allow this to be used to edit already existing sessions
# Add if/else check of whether a session already exists for the Session ID.
# If it is absent, open the files and meta data from there. Else, use the data that already exists in the database
class Confirm(LoginRequiredMixin, View):
    def get(self, request, session_data_id):
        session_data = SessionData.objects.get(id=session_data_id)
        dustrak_file_url = session_data.sensor_file.url

        # TODO: Must be port 8000. This may be due to NGINX. For production, this base domain and port should
        # be from a variable, rather than hardcoded
        dustrak_file_open = urllib.request.urlopen(f"http://localhost:8000{dustrak_file_url}")
        # TODO: From here, the relavant header data should be extracted and set to variables.
        # The dustrak file has a load_dustrak script that will help with the extraction of data
        default_timezone = 'America/Los_Angeles'
        # dustrak_file_content = load_dustrak(dustrak_file_read, default_timezone)
        # dustrak_file_header = dustrak_file_content[0]

        # TODO: Values extracted from the csv file will be combined with already known values
        # (ie: default time zone and logged in user)
        # These variables will be set as the initial values for the form, here
        form = ConfirmForm(initial={
            'collected_by': User.objects.get(id=request.user.id),
            'dustrak_file_url': dustrak_file_url,
            'timezone': default_timezone
        })

        return render(self.request, 'air_quality/confirm.html', {
            'session_data': session_data,
            'form': form
        })

    # TODO: Create a "post" function
    # TODO: Accept the parsed dusTrak data as an argument in the "post" function
    # If user submitted timezone is different from the default_timezone, rerun load_dustrak script to get new values.
    # Else, get values from dusTrak argument

    # TODO: Save data to the database, include air quality measurements
    # TODO: Redirect to a view of the Air Quality measurements


class ViewSessionData(View):
    """Provide temporary development page to view all uploaded SessionDatas."""
    def get(self, request):
        session_data_list = SessionData.objects.all()
        return render(self.request, 'air_quality/view.html', {
            'session_data_list': session_data_list
        })
