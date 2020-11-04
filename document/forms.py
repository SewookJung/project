from django import forms
from .models import Document, DocumentBasicForm


class DocumentForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ('client', 'category', 'mnfacture', 'product')
        widgets = {
            'client': forms.Select(attrs={'class': 'selectpicker', 'title': "고객사", 'id': 'client', 'data-live-search': 'true', 'data-container': 'body'}),
            'category': forms.Select(attrs={'class': 'selectpicker', 'title': "구 분", 'id': 'category', 'data-container': 'body'}),
            'mnfacture': forms.Select(attrs={'class': 'selectpicker', 'title': "제조사", 'id': 'mnfacture', 'data-live-search': 'true', 'data-container': 'body'}),
            'product': forms.Select(attrs={'class': 'selectpicker', 'title': "제품명", 'id': 'product', 'data-live-search': 'true', 'data-container': 'body'}),
        }


class DocumentBasicForms(forms.ModelForm):

    class Meta:
        model = DocumentBasicForm
        fields = ('title','description')
        widgets = {
            'title': forms.TextInput(attrs={'type': 'text', 'id': 'title', 'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'ex) 공용_제품명_문서명'}),
            'description': forms.TextInput(attrs={'type': 'text', 'id': 'description', 'class': 'form-control', 'autocomplete': 'off', }),
        }