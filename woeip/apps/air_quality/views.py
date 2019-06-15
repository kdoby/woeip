import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from .forms import SessionDataForm, SessionForm
from .models import SessionData, User
from .dustrak import load_dustrak

# Settings to access static media
import os
from django.conf import settings
from django.conf.urls.static import static

# from settings import PUBLIC_ROOT
from django.utils.encoding import force_text
import urllib
import pandas

logger = logging.getLogger(__name__)


class Upload(LoginRequiredMixin, View):
    def get(self, request):
        """Present file upload form to user"""
        return render(self.request, 'air_quality/upload.html', {
            'form': SessionDataForm
        })

    def post(self, request):
        """Save files to SessionData table"""
        files = self.request.FILES
        form = SessionDataForm(self.request.POST, files)
        if form.is_valid():
            sessionData = form.save()
            messages.add_message(self.request, messages.SUCCESS, 'Files successfully uploaded')
            path = redirect('review_upload', sessionData_id = sessionData.id)
        else:
            messages.add_message(self.request, messages.ERROR, 'File upload error')
            path = render(self.request, 'air_quality/upload.html', {
                'form': SessionDataForm
            })
        return path


# TODO: Add logic to allow this to be used to edit already existing sessions
# Add if/else check of whether a session already exists for the Session ID.
# If it is absent, open the files and meta data from there. Else, use the data that already exists in the database
# TODO: Open Dustrak CSV file to extract key values
class ReviewUpload(LoginRequiredMixin, View):
    def get(self, request, sessionData_id):
        # Get header from dustrak file
        default_timezone = 'America/Los_Angeles'
        # sessionData_upload = SessionData.objects.values_list('upload', flat=True).get(id=sessionData_id)
        sessionData = SessionData.objects.get(id=sessionData_id)
        dustrak_file_url = sessionData.upload.url
        # dustrak_file_url = f"{settings.MEDIA_URL}{sessionData_upload}"
        
        # TODO: Issue with media folder not seeming to exist
        # TODO: Fix path to file
        dustrak_file_open = open(f"./woeip{dustrak_file_url}", mode='r')
        dustrak_file_read = force_text(dustrak_file_open.read())
        # dustrak_file_content = load_dustrak(dustrak_file_read, default_timezone)
        # dustrak_file_header = dustrak_file_content[0]
        # dustrak_file_url = urllib.request.OpenerDirector(f"http://localhost{dustrak_file_url}")
        # dustrak_file_request = urllib.request.Request(dustrak_file_url)
        # dustrak_file_open = urllib.request.urlopen(dustrak_file_request)
        # dustrak_file_read = force_text(dustrak_file_open.read())



        # dustrak_file_content = load_dustrak(dustrak_file_read, default_timezone)
        # dustrak_file_header = dustrak_file_content[0]

        form = SessionForm(initial= {
            'collected_by': User.objects.get(id=request.user.id),
            'dustrak_file_url': dustrak_file_url,
            'timezone': default_timezone
        })

        # TODO: Reload data contents, if timezone is different
        return render(self.request, 'air_quality/review_upload.html', {
            'sessionData_id': sessionData_id,
            'dustrak_file_url': dustrak_file_url,
            'form': form
        })


class ViewSessionData(View):
    """Provide temporary development page to view all uploaded SessionDatas."""
    def get(self, request):
        session_data_list = SessionData.objects.all()
        return render(self.request, 'air_quality/view.html', {
            'session_data_list': session_data_list
        })
