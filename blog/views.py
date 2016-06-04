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

    


def toggle(request):




    return 



def open_image(request):

    data = dict()

    data['image-url'] = os.path.join('static', 'tmp', request.GET.get('image-url'))

    print request.GET.get('image-url')

    return JsonResponse(data)


def binary(request):

    response = dict()

    filename = request.GET.get('filename')

    print filename

    version = int(request.GET.get('current-version'))

    directory = os.path.join('files', filename.split('/')[1])

    
    image = cv2.imread(os.path.join(directory, str(version) + '.jpg' ), 0)

    # Binary

    ret, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

    # save file

    version += 1 # 

    path = os.path.join(directory , str(version) + '.jpg')

    cv2.imwrite(path, image)

    # response

    response['current-version'] = str(version)

    response['filename'] = path

    return JsonResponse(response)




def handle_uploaded_file(f):

    day, time = str(datetime.now()).split()

    time = day + time.replace(':','-').replace('.','-')

    os.mkdir(os.path.join('files', time))


    directory = os.path.join('files', time );
    filename = os.path.join(directory, '0.jpg');

    if os.path.isfile(filename):

        print 'already exist'

    with open(filename, 'wb+') as destination:

        for chunk in f.chunks():

            destination.write(chunk)   

    return filename, directory


def upload_file(request):

    if request.method == 'POST':

        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():

            original, filename = handle_uploaded_file(request.FILES['image'])

            response = {}

            response['original'] = original
            response['filename'] = filename

            return JsonResponse(response)
    
    else:


        form = ImageUploadForm()

    return render(request, 'upload.html', {'form': form})
    

def files(request, filename):

    import mimetypes

    filename = os.path.join('files', filename)
    download_name = 'test.jpg'
    wrapper = FileWrapper(open(filename))
    content_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(wrapper, content_type = content_type)
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment; filename=%s' %download_name
    
    return response



def canny(request):

    response = dict()

    filename = request.GET.get('filename')

    version = int(request.GET.get('current-version'))

    directory = os.path.join('files', filename.split('/')[1])

    image = cv2.imread(os.path.join(directory, str(version) + '.jpg' ), 0)

    TH = int(request.GET.get('TH'))

    TL = int(request.GET.get('TL'))

    # Binary

    image = cv2.Canny(image,TL, TH)

    # save file

    version += 1 # 

    path = os.path.join(directory , str(version) + '.jpg')

    cv2.imwrite(path, image)

    # response

    response['current-version'] = str(version)

    response['filename'] = path

    return JsonResponse(response)





def blur(request):

    filename = request.GET.get('filename')

    image, response = process(request)

    # value 

    kernel = int(request.GET.get('blur-kernel'))

    image = cv2.blur(image, (kernel,kernel))

    cv2.imwrite(response['filename'], image)

    return JsonResponse(response)



def process(request, color = True):

    response = dict()

    filename = request.GET.get('filename')

    version = int(request.GET.get('current-version'))

    directory = os.path.join('files', filename.split('/')[1])

    image = cv2.imread(os.path.join(directory, str(version) + '.jpg' ), color)
    
    version += 1 # 
    
    path = os.path.join(directory , str(version) + '.jpg')
    
    response['current-version'] = str(version)
    
    response['filename'] = path

    return image, response



def GaussianBlur(request):

    filename = request.GET.get('filename')

    image, response = process(request)

    # value 

    kernel = int(request.GET.get('GaussianBlur-kernel'))

    image = cv2.blur(image, (kernel,kernel))

    cv2.imwrite(response['filename'], image)

    return JsonResponse(response)


def medianBlur(request):

    filename = request.GET.get('filename')

    image, response = process(request)

    # value 

    kernel = int(request.GET.get('medianBlur-kernel'))

    image = cv2.blur(image, (kernel,kernel))

    cv2.imwrite(response['filename'], image)

    return JsonResponse(response)
