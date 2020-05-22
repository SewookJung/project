from django import forms
from .models import Project, Document, DocumentAttachment


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('client', 'product', 'status')
        widgets = {
            'client': forms.Select(attrs={'class': 'selectpicker', 'title': '고객사 선택', 'id': 'client_id', 'data-live-search': 'true'}),
            'status': forms.Select(attrs={'class': 'selectpicker', 'title': '진행 여부 선택', 'id': 'status'})
        }


class DocumentForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ('project', 'kind')
        widgets = {
            'project': forms.Select(attrs={'class': 'selectpicker',  'id': 'project'}),
            'kind': forms.Select(attrs={'class': 'selectpicker',  'id': 'kind'}),
        }


class DocumentAttachmentForm(forms.ModelForm):

    class Meta:
        model = DocumentAttachment
        fields = ['attach']

    def __init__(self, *args, **kwargs):
        super(DocumentAttachmentForm, self).__init__(*args, **kwargs)
        self.fields['attach'].required = False
