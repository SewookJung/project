from django import forms
from .models import Project, Document, DocumentAttachment


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('client', 'status')
        widgets = {
            'client': forms.Select(attrs={'class': 'selectpicker', 'title': '고객사 선택', 'id': 'client_id', 'data-live-search': 'true'}),
            'status': forms.Select(attrs={'class': 'selectpicker', 'title': '진행 여부 선택', 'id': 'status'})
        }


class DocumentForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ('project', 'kind', 'pre_middle_class', 'pro_middle_class',
                  'exa_middle_class', 'etc_middle_class', 'man_middle_class')
        widgets = {
            'project': forms.Select(attrs={'class': 'selectpicker',  'id': 'project'}),
            'kind': forms.Select(attrs={'class': 'selectpicker',  'id': 'kind'}),
            'pre_middle_class': forms.Select(attrs={'class': 'selectpicker middle-class',  'id': 'preMiddleClass'}),
            'pro_middle_class': forms.Select(attrs={'class': 'selectpicker middle-class',  'id': 'proMiddleClass'}),
            'exa_middle_class': forms.Select(attrs={'class': 'selectpicker middle-class',  'id': 'exaMiddleClass'}),
            'etc_middle_class': forms.Select(attrs={'class': 'selectpicker middle-class',  'id': 'etcMiddleClass'}),
            'man_middle_class': forms.Select(attrs={'class': 'selectpicker middle-class',  'id': 'manMiddleClass'}),
        }


class DocumentAttachmentForm(forms.ModelForm):

    class Meta:
        model = DocumentAttachment
        fields = ['attach']

    def __init__(self, *args, **kwargs):
        super(DocumentAttachmentForm, self).__init__(*args, **kwargs)
        self.fields['attach'].required = False
