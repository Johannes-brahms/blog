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
from blog.views import article, files, image, open_image, binary, upload_pic, upload_file

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^blog/(?P<title>.*)$', article),
    url(r'^image$', image),
    
    url(r'^open$', open_image),
    url(r'^binary$', binary),
    url(r'^upload_pic$', upload_pic),
    url(r'^upload_file$', upload_file),
    url(r'^files/(?P<filename>.*)$', files)
    #url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]
