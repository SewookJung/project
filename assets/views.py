from django.shortcuts import render
from assets.models import Asset
from django.db.models import Q


def assets_main(request):
    assets = Asset.objects.all()
    return render(request, 'assets_main/assets_main.html', {'assets': assets})


def assets_add(request):
    return render(request, 'assets_main/assets_add.html', {})


def assets_status(request):
    assets = Asset.objects.all()
    assets_keep = Asset.objects.filter(is_state='5')
    assets_rent = Asset.objects.filter(is_state='3')
    return render(request, 'assets_main/assets_status.html', {'assets': assets, 'assets_keep': assets_keep, 'assets_rent': assets_rent})
