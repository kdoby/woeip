import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from .forms import DocumentForm
from .models import Document

logger = logging.getLogger(__name__)


class Upload(LoginRequiredMixin, View):
    def get(self, request):
        documents_list = Document.objects.all()
        return render(self.request, 'air_quality/upload.html', {'documents': documents_list})

    def post(self, request):
        files = self.request.FILES
        # logger.log(len(files))
        form = DocumentForm(self.request.POST, files)
        if form.is_valid():
            document = form.save()
            data = {'is_valid': True, 'description': document.file.name, 'url': document.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


# @login_required
# def upload(request):
#     """Upload data for a session collected using the Dustrak air quality device and a separate GPS
#     log file.
#     """
#     if request.method == 'POST':
#         form = forms.DocumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('view_files')
#     else:
#         form = forms.DocumentForm()
#     return render(request, 'air_quality/upload.html', { 'form' : form })

# def view_files(request):
#     documents = models.Document.objects.all()
#     return render(request, 'air_quality/view_files.html', { 'documents': documents })
