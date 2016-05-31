from __future__ import unicode_literals

from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.


class Category(models.Model):
    
    name = models.CharField(u'Name', max_length = 50)
    
    def __unicode__(self):
        return self.name

class Article(models.Model):
    
    title = models.CharField(u'Title', max_length = 50)
    content = RichTextField(config_name = 'awesome_ckeditor')
    
    category = models.ForeignKey('Category', blank = True, null = True)
     
    def __unicode__(self):
        return self.title




class Document(models.Model):
    image = models.FileField(upload_to = 'image/%Y/%m/%d')

class ExampleModel(models.Model):

    model_pic = models.ImageField(upload_to = 'upload/%Y')