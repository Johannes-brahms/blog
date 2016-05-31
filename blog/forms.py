from django import forms

class DocumentForm(forms.Form):
    files = forms.FileField(
            label = 'Select a file',)

    

class UploadFileForm(forms.Form):

    title = forms.CharField(max_length = 50)
    image = forms.FileField()



class ImageUploadForm(forms.Form):

	image = forms.FileField()

