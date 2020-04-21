from django import forms

from .models import Asset, Assetrent
from utils.constant import STATUS_PERSONAL, STATUS_TEST, STATUS_RENTAL, STATUS_DISPOSAL, STATUS_KEEP


class AssetForm(forms.ModelForm):

    class Meta:
        model = Asset
        fields = ('comments', 'closed', 'member_name', 'mnfacture', 'model',
                  'cpu', 'memory', 'harddisk', 'is_where', 'is_state', 'purchase_date', 'serial')

        widgets = {
            'member_name': forms.Select(attrs={'class': 'selectpicker', 'title': '대여자 선택', 'id': 'member_id'}),
            'comments': forms.Textarea(attrs={'class': 'form-control col-sm-12', 'rows': '5', 'id': 'comment'}),
            'purchase_date': forms.TextInput(attrs={'type': 'text', 'id': 'datepicker1', 'class': 'form-control calendar__start', 'autocomplete': 'off', 'class': 'form-control'}),
            'is_where': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'ex) 남부팀, 본사, 원주(인터넷망), 원주(업무망)', 'autocomplete': 'off'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'ZenBook-UX362FA_UX362FA'}),
            'harddisk': forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': '256GB'}),
            'memory': forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': '16GB'}),
            'cpu': forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'intel(R) Core(TM) i5-8250U CPU @ 1.6Ghz 1.80GHz'}),
            'mnfacture': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'ex) LG, ASUS', 'autocomplete': 'off'}),
            'serial': forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'ex) N0CV1905MB0083116 '}),
            'is_state': forms.Select(attrs={'class': 'selectpicker', 'title': '자산상태', 'id': 'asset_is-state'},
                                     choices=[
                (STATUS_PERSONAL, "개인사용"),
                (STATUS_TEST, "테스트"),
                (STATUS_RENTAL, "대여중"),
                (STATUS_DISPOSAL, "폐기"),
                (STATUS_KEEP, "보관"),
            ]),
        }


class AssetrentForm(forms.ModelForm):

    class Meta:
        model = Assetrent
        fields = ('asset', 'stdate',
                  'eddate', 'member_name', 'comments')

        widgets = {
            'asset': forms.TextInput(attrs={'type': 'text', 'class': 'form-control asset-name', 'readonly': 'readonly'}),
            'comments': forms.Textarea(attrs={'class': 'form-control col-sm-12', 'rows': '5'}),
            'stdate': forms.TextInput(attrs={'type': 'text', 'id': 'datepicker1', 'class': 'form-control calendar__start', 'autocomplete': 'off'}),
            'eddate': forms.TextInput(attrs={'type': 'text', 'id': 'datepicker2', 'class': 'form-control calendar__start', 'autocomplete': 'off'}),
            'member_name': forms.TextInput(attrs={'class': 'form-control', 'type': 'text', }),
        }
