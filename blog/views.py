from django.shortcuts import render, render_to_response

from django.http import HttpResponse, HttpResponseNotModified, Http404, JsonResponse, HttpResponseRedirect
from django.conf import settings
from blog.models import Article, Document, ExampleModel
from .forms import DocumentForm, UploadFileForm, ImageUploadForm
from wsgiref.util import FileWrapper
from datetime import datetime

from skimage import segmentation, io, morphology

import urllib
import json
import cv2
import os
import shutil
import numpy as np
from matplotlib import pyplot as plt
from scipy import ndimage
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

    return render(
            request,
            'image.html')

def files(request, filename):

    import mimetypes
    download_name = filename
    filename = os.path.join('files', filename)
    wrapper = FileWrapper(open(filename))
    content_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(wrapper, content_type = content_type)
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment; filename=%s' %download_name
    
    return response

# function 

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
    
def download(request):

    import mimetypes

    filename = request.GET.get('filename')

    version = int(request.GET.get('current-version'))

    directory = os.path.join(filename.split('/')[1])

    print directory

    download_name = directory + '.jpg'

    wrapper = FileWrapper(open(os.path.join('files',directory, str(version) + '.jpg' )))

    content_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(wrapper, content_type = content_type)
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment; filename=%s' %download_name
    
    return response

def process(request, color = True):

    response = dict()

    filename = request.GET.get('filename')

    version = int(request.GET.get('current-version'))

    directory = os.path.join('files', filename.split('/')[1])

    image = cv2.imread(os.path.join(directory, str(version) + '.jpg' ), color)
    
    version += 1 # 
    
    p = os.path.join(directory , str(version) + '.jpg')
    
    response['current-version'] = str(version)
    
    response['filename'] = p

    response['directory'] = directory

    return image, response

def skread(request, color = True):

    response = dict()

    filename = request.GET.get('filename')

    version = int(request.GET.get('current-version'))

    directory = os.path.join('files', filename.split('/')[1])

    image = io.imread(os.path.join(directory, str(version) + '.jpg' ))
    
    version += 1 # 
    
    p = os.path.join(directory , str(version) + '.jpg')
    
    response['current-version'] = str(version)
    
    response['filename'] = p

    response['directory'] = directory

    return image, response


# OpenCV function

def canny(request):

    image, response = process(request)

    TH = int(request.GET.get('TH'))

    TL = int(request.GET.get('TL'))

    # Binary

    image = cv2.Canny(image,TL, TH)

    # save file

    cv2.imwrite(response['filename'], image)

    return JsonResponse(response)

def blur(request):

    image, response = process(request)

    # value 

    kernel = int(request.GET.get('blur-kernel'))

    image = cv2.blur(image, (kernel,kernel))

    cv2.imwrite(response['filename'], image)

    return JsonResponse(response)

def GaussianBlur(request):

    image, response = process(request)

    # value 

    kernel = int(request.GET.get('GaussianBlur-kernel'))

    image = cv2.blur(image, (kernel,kernel))

    cv2.imwrite(response['filename'], image)

    return JsonResponse(response)

def medianBlur(request):

    image, response = process(request)

    # value 

    kernel = int(request.GET.get('medianBlur-kernel'))

    image = cv2.blur(image, (kernel,kernel))

    cv2.imwrite(response['filename'], image)

    return JsonResponse(response)

def binary(request):

    image, response = process(request, color = False)

    threshold = int(request.GET.get('binary-threshold'))

    ret, image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)

    cv2.imwrite(response['filename'], image)

    return JsonResponse(response)


def otsu(request):

    from skimage.filters import threshold_otsu

    image, response = skread(request)

    thresh = threshold_otsu(image)

    image = image > thresh

    image = image.astype(np.uint8) * 255

    io.imsave(response['filename'], image)

    return JsonResponse(response)

def erode(request):

    image, response = process(request)

    kernel = int(request.GET.get('Erosion-Kernel'))

    kernel = np.ones((kernel,kernel),np.uint8)

    iteration = int(request.GET.get('Erosion-Iteration'))

    print 'type : ',type(image)

    image = cv2.erode(image,kernel,iterations = iteration)

    cv2.imwrite(response['filename'], image)

    return JsonResponse(response)

def dilate(request):

    image, response = process(request)

    kernel = int(request.GET.get('Dilation-Kernel'))

    kernel = np.ones((kernel,kernel),np.uint8)

    iteration = int(request.GET.get('Dilation-Iteration'))

    image = cv2.dilate(image,kernel,iterations = iteration)

    cv2.imwrite(response['filename'], image)

    return JsonResponse(response)

def opening(request):

    image, response = process(request)

    kernel = int(request.GET.get('Opening-Kernel'))

    kernel = np.ones((kernel,kernel),np.uint8)

    image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

    cv2.imwrite(response['filename'], image)

    return JsonResponse(response)

def closing(request):

    image, response = process(request)

    kernel = int(request.GET.get('Closing-Kernel'))

    kernel = np.ones((kernel,kernel),np.uint8)

    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

    cv2.imwrite(response['filename'], image)

    return JsonResponse(response)

def Morphological_Gradient(request):

    image, response = process(request)

    kernel = int(request.GET.get('Morphological-Gradient-Kernel'))

    kernel = np.ones((kernel,kernel),np.uint8)

    image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel)

    cv2.imwrite(response['filename'], image)

    return JsonResponse(response)

def sobel(request):

    image, response = process(request)

    kernel = int(request.GET.get('Sobel-Kernel'))

    X = int(request.GET.get('Sobel-X'))

    Y = int(request.GET.get('Sobel-Y'))

    image = cv2.Sobel(image, cv2.CV_8U, X, Y, ksize = kernel)

    cv2.imwrite(response['filename'], image)

    return JsonResponse(response)

def felzenszwalb(request):

    image, response = process(request, color = True)

    if len(image.shape) == 2:
        
        image = cv2.cvtColor(image,cv2.COLOR_GRAY2RGB)

    scale = int(request.GET.get('felzenszwalb-scale'))

    sigma = float(request.GET.get('felzenszwalb-sigma'))

    min_size = int(request.GET.get('felzenszwalb-min'))  

    segments = segmentation.felzenszwalb(image, scale = scale, sigma = sigma, min_size = min_size)

    image = segmentation.mark_boundaries(image, segments)

    io.imsave(response['filename'], image)

    return JsonResponse(response)

def grayscale(request):

    from skimage.color import rgb2gray

    image, response = process(request, color = False)

    print 'grayscale'

    image = rgb2gray(image)

    cv2.imwrite(response['filename'], image)

    return JsonResponse(response)

def negative(request):

    image, response = process(request, color = False)

    image = 255 - image

    cv2.imwrite(response['filename'], image)

    return JsonResponse(response)

def fusion(request):

    image, response = process(request, color = True)

    original = cv2.imread(os.path.join(response['directory'], '0.jpg'), True)
    
    original = original * (image > 128)
    
    original.astype(int) 
    
    cv2.imwrite(response['filename'], original)

    return JsonResponse(response)

def slic(request):

    image, response = skread(request)

    if len(image.shape) == 2:
        
        image = cv2.cvtColor(image,cv2.COLOR_GRAY2RGB)

    n = int(request.GET.get('slic-n'))

    sigma = float(request.GET.get('slic-sigma'))

    compactness = int(request.GET.get('slic-compactness')) 

    segments = segmentation.slic(image, n_segments = n, compactness = compactness, sigma = sigma)

    image = segmentation.mark_boundaries(image, segments)

    io.imsave(response['filename'], image)

    return JsonResponse(response)

def quickshift(request):

    image, response = skread(request)

    if len(image.shape) == 2:
        
        image = cv2.cvtColor(image,cv2.COLOR_GRAY2RGB)

    kernel = int(request.GET.get('quickshift-kernel'))

    dist = int(request.GET.get('quickshift-max-dist'))

    ratio = float(request.GET.get('quickshift-ratio')) 

    segments = segmentation.quickshift(image, kernel_size = kernel, max_dist = dist, ratio = ratio)

    image = segmentation.mark_boundaries(image, segments)

    io.imsave(response['filename'], image)

    return JsonResponse(response)

def fillhole(request):

    from scipy import ndimage as ndi

    image, response = process(request)

    image = ndi.binary_fill_holes(image)

    plt.imsave(response['filename'], image)

    return JsonResponse(response)
"""
def watershed(request):

    img, response = process(request)

    b,g,r = cv2.split(img)

    rgb_img = cv2.merge([r,g,b])

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    # noise removal
    kernel = np.ones((2,2),np.uint8)
    #opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)
    closing = cv2.morphologyEx(thresh,cv2.MORPH_CLOSE,kernel, iterations = 2)

    # sure background area
    sure_bg = cv2.dilate(closing,kernel,iterations=3)

    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(sure_bg,cv2.DIST_L2,3)

    # Threshold
    ret, sure_fg = cv2.threshold(dist_transform,0.1*dist_transform.max(),255,0)

    # Finding unknown region
    sure_fg = np.uint8(sure_fg)

    unknown = cv2.subtract(sure_bg,sure_fg)

    # Marker labelling
    ret, markers = cv2.connectedComponents(sure_fg)

    # Add one to all labels so that sure background is not 0, but 1
    markers = markers+1

    # Now, mark the region of unknown with zero
    markers[unknown==255] = 0

    markers = cv2.watershed(img,markers)
    img[markers == -1] = [255,255,255]

    cv2.imwrite(response['filename'], img)

    return JsonResponse(response)
"""


def watershed(request):

    from skimage.morphology import watershed

    from skimage.feature import peak_local_max

    image, response = process(request, False)
    
    distance = ndimage.distance_transform_edt(image)

    local_maxi = peak_local_max(distance, indices=False, footprint=np.ones((3, 3)), labels=image)
    
    markers = morphology.label(local_maxi)

    labels_ws = watershed(-distance, markers, mask=image)

    image = segmentation.mark_boundaries(image, labels_ws)

    plt.imsave(response['filename'], image)

    return JsonResponse(response)

def histogram(request):

    image, response = process(request, False)

    image = cv2.equalizeHist(image)

    cv2.imwrite(response['filename'], image)

    return JsonResponse(response)

def log(request):

    image, response = process(request, False)

    constant = float(request.GET.get('log-constant'))

    image = (constant * np.log10(image) * 255).astype(np.uint8)

    cv2.imwrite(response['filename'], image)

    return JsonResponse(response)

def powerlaw(request):

    image, response = process(request, False)

    constant = float(request.GET.get('powerlaw-constant'))
    
    gamma = float(request.GET.get('powerlaw-gamma'))

    image = (constant * image ** (gamma) * 255).astype(np.uint8)

    cv2.imwrite(response['filename'], image)

    return JsonResponse(response)

def gaussian(request):

    image, response = process(request, False)

    mean = int(request.GET.get('gaussian-mean'))

    deviation = int(request.GET.get('gaussian-deviation'))

    noise = np.random.normal(mean, deviation ** 0.5 ,image.shape)
    
    image = image + noise

    cv2.imwrite(response['filename'], image)

    return JsonResponse(response)

def rayleigh(request):

    image, response = process(request, False)

    scale = int(request.GET.get('rayleigh-scale')) 

    noise = np.random.rayleigh(scale, image.shape)
    
    image = image + noise

    cv2.imwrite(response['filename'], image)

    return JsonResponse(response)

def gamma(request):

    image, response = process(request, False)

    shape = int(request.GET.get('gamma-shape')) 
    scale = int(request.GET.get('gamma-scale')) 

    noise = np.random.gamma(shape, scale, image.shape)
    
    image = image + noise

    cv2.imwrite(response['filename'], image)

    return JsonResponse(response)

def exponential(request):

    image, response = process(request, False)

    scale = int(request.GET.get('exponential-scale')) 

    noise = np.random.exponential(scale, image.shape)
    
    image = image + noise

    cv2.imwrite(response['filename'], image)

    return JsonResponse(response)

def uniform(request):

    image, response = process(request, False)

    low = float(request.GET.get('uniform-low')) 

    high = float(request.GET.get('uniform-high')) 

    noise = np.random.uniform(0, 40, image.shape)

    for y in xrange(image.shape[0]):

        for x in xrange(image.shape[1]):

            if image[y][x] + noise[y][x] > 255:

                image[y][x] = 255

            elif image[y][x] + noise[y][x] < 0:

                image[y][x] = 0

            else:

                image[y][x] = image[y][x] + noise[y][x]


    cv2.imwrite(response['filename'], image)

    return JsonResponse(response)

def SaltPepper(request):

    from skimage.util import random_noise

    image, response = process(request, False)

    image = random_noise(image, mode = 's&p')

    io.imsave(response['filename'], image)

    return JsonResponse(response)

def PlotHistogram(request):

    from matplotlib import pyplot as plt

    image, response = process(request, False)

    plt.hist(image.ravel(),256,[0,256])

    plt.ylim([0,1800])

    plt.xlim([0,256])
    
    plt.savefig(response['filename'])

    plt.close()

    return JsonResponse(response)

def meanshift(request):

    image, response = process(request)

    spatial = int(request.GET.get('meanshift-Spatial')) 

    color = int(request.GET.get('meanshift-Color')) 

    image = cv2.pyrMeanShiftFiltering(image, spatial, color)

    io.imsave(response['filename'], image)

    return JsonResponse(response)