from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('client', 'product', 'model', 'status')
        widgets = {
            'client': forms.Select(attrs={'class': 'selectpicker', 'title': '고객사 선택', 'id': 'client_id'}),
            'product': forms.Select(attrs={'class': 'selectpicker', 'title': '제품 선택', 'id': 'product_id'}),
            'model': forms.Select(attrs={'class': 'selectpicker', 'title': '제품 선택', 'id': 'model_id'}),
            'status': forms.Select(attrs={'class': 'selectpicker', 'title': '진행 여부 선택', 'id': 'status'})
        }
