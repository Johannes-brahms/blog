"""heidiz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include, url
from django.contrib import admin
from blog.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^blog/(?P<title>.*)$', article),
    url(r'^image$', image),
    
    url(r'^open$', open_image),

    #url(r'^upload_pic$', upload_pic),
    url(r'^upload_file$', upload_file),
    url(r'^files/(?P<filename>.*)$', files),

    url(r'^download$', download),

    # opencv function

    url(r'^binary$', binary),
    url(r'^blur$', blur),
    url(r'^canny$', canny),
    url(r'^GaussianBlur$', GaussianBlur),
    url(r'^medianBlur$', medianBlur),
    url(r'^erode$', erode),
    url(r'^dilate$', dilate),
    url(r'^opening$', opening),
    url(r'^closing$', closing),
    url(r'^sobel$', sobel),
    url(r'^Morphological-Gradient$', Morphological_Gradient),
    #url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]
