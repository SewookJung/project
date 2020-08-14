from django import forms
from .models import Equipment


class EquipmentForm(forms.ModelForm):

    class Meta:
        model = Equipment
        fields = ('client', 'product_model', 'mnfacture')
        widgets = {
            'client': forms.Select(attrs={'class': 'selectpicker', 'title': "고객사", 'id': 'client_id', 'data-live-search': 'true'}),
            'product_model': forms.Select(attrs={'class': 'selectpicker', 'title': "제조사", 'id': 'product-model', 'data-live-search': 'true'}),
            'mnfacture': forms.Select(attrs={'class': 'selectpicker', 'title': "모델명", 'id': 'mnfacture', 'data-live-search': 'true', 'data-container': 'body'}),
        }
