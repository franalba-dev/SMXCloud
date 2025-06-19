from django import forms
from Documents.models import Document, Subject

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = '__all__'
        exclude = ['owner']

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'