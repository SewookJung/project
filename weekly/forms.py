from django import forms
from .models import Report


class ReportForm(forms.ModelForm):

    class Meta:
        model = Report
        fields = ('client', 'product', 'sales_type', 'client_manager')
        widgets = {
            'client': forms.Select(attrs={'class': 'selectpicker', 'title': '고객사 선택', 'id': 'client_id', 'data-live-search': 'true'}),
            'product': forms.Select(attrs={'class': 'selectpicker', 'title': '제품 선택', 'id': 'product_id'}),
            'sales_type': forms.Select(attrs={'class': 'selectpicker', 'title': '세일즈 선택', 'id': 'sales_type_id'}),
            'client_manager': forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'id': 'client_manager', 'autocomplete': 'off'}),
        }
