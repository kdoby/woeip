import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from .forms import SessionDataForm
from .models import SessionData

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
class ReviewUpload(LoginRequiredMixin, View):
    def get(self, request, sessionData_id):
        return render(self.request, 'air_quality/review_upload.html', {
            'sessionData_id': sessionData_id
        })


class ViewSessionData(View):
    """Provide temporary development page to view all uploaded SessionDatas."""
    def get(self, request):
        sessionData_list = SessionData.objects.all()
        return render(self.request, 'air_quality/view_data.html', {
            'sessionData': sessionData_list,      
        })
    # context = {'cleanup': get_object_or_404(Cleanup, id=kwargs['pk'])}
    # return render(request, 'cleanups/edit.html', context)