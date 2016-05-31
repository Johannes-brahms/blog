from django.shortcuts import render, render_to_response

from django.http import HttpResponse, HttpResponseNotModified, Http404, JsonResponse, HttpResponseRedirect
from django.conf import settings
from blog.models import Article, Document, ExampleModel
from .forms import DocumentForm, UploadFileForm, ImageUploadForm
from wsgiref.util import FileWrapper
from datetime import datetime


import urllib
import json
import cv2
import os

BASE_DIR  = settings.BASE_DIR

tmp = os.path.join('static', 'tmp')



# Create your views here.

def hello_world(request):
    return HttpResponse('Hello world')

def article(request, title):
    
    try:
        article = Article.objects.get(title = title)
    except:
        raise Http404("This page does not exist")


    return render(
            request, 
            'blog.html',
            {'article': article })





def image(request):

    if request.is_ajax():

        message = 'yes, Ajax'

    else:
        message = 'No Ajax'

    return render(
            request,
            'image.html')

    




def open_image(request):

    data = dict()

    data['image-url'] = os.path.join('static', 'tmp', request.GET.get('image-url'))

    print request.GET.get('image-url')

    

    return JsonResponse(data)


def binary(request):

    response = dict()

    filename = request.GET.get('filename')
    version = request.GET.get('current-version')

    print '[filename] : ', filename
    print '[version] : ', version 

    try:
        version = int(version) + 1

    except:
        raise


    #response['filename'] = os.path.join('static', 'tmp', request.GET.get('image-url'))

    original = os.path.join(BASE_DIR, filename)
    
    image = cv2.imread(original, 0)

    save = os.path.join(BASE_DIR, 'files', filename.split('/')[-1].split('.')[0], str(version) + '.jpg')

    print '[save path] : ', save
    ret, binary = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)


    cv2.imwrite(save, binary)

    response['current-version'] = str(version)

    return JsonResponse(response)




            
def upload_pic(request):

    if request.method == 'POST':      

        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():

            print 'is valid'

            m = ExampleModel.objects.get(pk = 0)
            m.model_pic = form.cleaned_data['image']
            m.save()

            return HttpResponse('image upload success')

        print 'not valid'

    return HttpResponseForbidden('allow only via PddOST')

    
def handle_uploaded_file(f):

    

    day, time = str(datetime.now()).split()

    time = day + time.replace(':','-').replace('.','-')

    filename = os.path.join('static','tmp', time + '.jpg')


    if os.path.isfile(filename):

        print 'already exist'

    with open(filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)   

    return filename 

def upload_file(request):
    print 'in upload_file view'

    print request.method

    if request.method == 'POST':

        form = ImageUploadForm(request.POST, request.FILES)
        #print form.cleaned_data
        print 'form : ', request.FILES
        print 'request'

        if form.is_valid():

            print 'is valid'


            filename = handle_uploaded_file(request.FILES['image'])

            response = {}
            response['filename'] = filename
            print response['filename']
            return JsonResponse(response)
    
    else:

        print 'Not POST'
        form = ImageUploadForm()

    return render(request, 'upload.html', {'form': form})
    

def files(request, filename):


    import mimetypes
    
    
    filename = os.path.join('files', filename)
    download_name = 'tst.png'
    wrapper = FileWrapper(open(filename))
    content_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(wrapper, content_type = content_type)
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment; filename=%s' %download_name
    return response
