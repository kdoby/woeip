import logging
import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from .forms import UploadForm
from .models import UploadedFile

logger = logging.getLogger(__name__)


class Upload(LoginRequiredMixin, View):

    def meets_requirements(self, documents_list):
        meets_reqs = False
        doc_exts = [os.path.splitext(doc.file.name)[1] for doc in documents_list]
        if '.log' in doc_exts and '.csv' in doc_exts and len(documents_list) == 2:
            meets_reqs = True
        return meets_reqs

    def get(self, request):
        documents_list = UploadedFile.objects.filter(uploaded_by=request.user, processed=False)
        if self.meets_requirements(documents_list):
            return redirect('submit')
        return render(request, 'air_quality/upload.html', {'documents': documents_list})

    def post(self, request):
        documents_list = UploadedFile.objects.filter(uploaded_by=request.user, processed=False)
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save()
            document.uploaded_by = request.user
            document.save()
            documents_list = UploadedFile.objects.filter(uploaded_by=request.user, processed=False)
            data = {
                'reqs_met': self.meets_requirements(documents_list),
                'is_valid': True, 
                'name': document.file.name, 
                'url': document.file.url, 
                'delete_url': 'delete/' + str(document.pk)}
            return JsonResponse(data)
        return render(request, 'air_quality/upload.html', {'documents': documents_list})


@login_required
def delete(request, document_id):
    documents_list = UploadedFile.objects.filter(uploaded_by=request.user, processed=False)
    document = UploadedFile.objects.get(pk=document_id)
    if document in documents_list:
        document.delete()
    return redirect('upload')

def submit(request):
    documents_list = UploadedFile.objects.filter(uploaded_by=request.user, processed=False)
    for doc in documents_list:
        doc.processed = True
        doc.save()
    # Create a session out of these documents!
    return HttpResponse(
        '<h1>Success uploading 1 Dustrak file and 1 GPS file</h5>'
        '<ul><li>%s</li></ul' % '</li><li>'.join(
            ['<a href="%s">%s</a>' % (doc.file.url, doc.file.name) for doc in documents_list]))
