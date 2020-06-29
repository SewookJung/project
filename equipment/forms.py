from django import forms
from .models import Equipment


class EquipmentForm(forms.ModelForm):

    class Meta:
        model = Equipment
        fields = ('client', 'product_model', 'mnfacture')
        widgets = {
            'client': forms.Select(attrs={'class': 'selectpicker', 'id': 'client_id', 'data-live-search': 'true'}),
            'product_model': forms.Select(attrs={'class': 'selectpicker', 'id': 'product-model', 'data-live-search': 'true'}),
            'mnfacture': forms.Select(attrs={'class': 'selectpicker', 'id': 'mnfacture', 'data-live-search': 'true'}),
        }
