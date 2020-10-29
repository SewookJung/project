from django import forms
from .models import Document


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