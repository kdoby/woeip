import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from .forms import UploadForm
from .models import UploadedFile

logger = logging.getLogger(__name__)


class Upload(LoginRequiredMixin, View):
    def get(self, request):
        documents_list = UploadedFile.objects.filter(uploaded_by=request.user, processed=False)
        return render(request, 'air_quality/upload.html', {'documents': documents_list})

    def post(self, request):
        documents_list = UploadedFile.objects.filter(uploaded_by=request.user, processed=False)
        form = UploadForm(request.POST, request.FILES)
        logger.info(request.FILES)
        if form.is_valid():
            document = form.save()
            document.uploaded_by = request.user
            document.save()
            data = {
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
    # Create a session out of these documents!
    return HttpResponse('success')