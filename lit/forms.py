from django import forms

class UploadFileForm(forms.Form):
    files  = forms.FileField()
    title_with_extension = forms.CharField(max_length = 20)
    
