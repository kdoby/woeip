import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from .forms import SessionDataForm, SessionForm
from .models import SessionData, User
from .dustrak import load_dustrak

from django.utils.encoding import force_text
import urllib

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
            path = redirect('upload')
        return path


# TODO: Add logic to allow this to be used to edit already existing sessions
# Add if/else check of whether a session already exists for the Session ID.
# If it is absent, open the files and meta data from there. Else, use the data that already exists in the database
# TODO: Open Dustrak CSV file to extract key values
class ReviewUpload(LoginRequiredMixin, View):
    def get(self, request, sessionData_id):
        # Get header from dustrak file
        default_timezone = 'America/Los_Angeles'
        session_data = SessionData.objects.get(id=sessionData_id)
        dustrak_file_location = urllib.request(session_data.upload.url)
        dustrak_file_read = force_text(dustrak_file_location.read())
        dustrak_file_content = load_dustrak(dustrak_file_read, default_timezone)
        dustrak_file_header = dustrak_file_content[0]

        form = SessionForm(initial= {
            'collected_by': User.objects.get(id=request.user.id),
            'timezone': default_timezone
        })

        # TODO: Reload data contents, if timezone is different
        return render(self.request, 'air_quality/review_upload.html', {
            'sessionData_id': sessionData_id,
            'dustrak_file_location': dustrak_file_location,
            'form': form
        })


class ViewSessionData(View):
    """Provide temporary development page to view all uploaded SessionDatas."""
    def get(self, request):
        sessionData_list = SessionData.objects.all()
        return render(self.request, 'air_quality/view_data.html', {
            'sessionData': sessionData_list,      
        })
