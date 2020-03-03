from django.shortcuts import render, redirect, get_object_or_404
from assets.models import Asset, Assetrent
from django.db.models import Q
from .forms import AssetForm, AssetrentForm
from datetime import datetime


def assets_main(request):
    assets = Asset.objects.exclude(is_state=4)
    return render(request, 'assets_main/assets_main.html', {'assets': assets})


def assets_add(request):
    form = AssetForm()
    return render(request, 'assets_main/assets_add.html', {'form': form})


def assets_status(request):
    assets_rent = Asset.objects.filter(is_state=3)
    assets_keep = Asset.objects.filter(is_state=5)
    rent_form = AssetForm()
    return render(request, 'assets_main/assets_status.html', {'assets_rent': assets_rent, 'rent_form': rent_form, 'assets_keep': assets_keep})


def assets_rent(request):
    if request.method == "POST":
        asset = Asset.objects.get(pk=request.POST['assetId'])
        asset.member_name_id = request.POST['memberId']
        asset.comments = request.POST['comments']
        asset.is_state = 3
        asset.save()
        asset_rent = Assetrent(stdate=request.POST['stDate'], eddate=request.POST['edDate'],
                               comments=request.POST['comments'], asset_id=request.POST['assetId'], member_name=request.POST['memberName'])
        asset_rent.save()
        return redirect('assets_status')
    else:
        return render(request, 'assets_main/assets_rent.html', {})


def assets_return(request):
    if request.method == "POST":
        asset_rent = Assetrent.objects.get(
            asset_id=request.POST['assetId'], return_date=None)
        asset_rent.return_date = datetime.now()
        asset_rent.save()
        asset = Asset.objects.get(pk=request.POST['assetId'])
        asset.is_state = 5
        asset.comments = ''
        asset.is_where = "본사"
        asset.member_name_id = 8
        asset.save()
        return redirect('assets_status')
    else:
        return render(request, 'assets_main/assets_status.html', {})


def assets_add_apply(request):
    if request.method == "POST":
        asset = Asset(mnfacture=request.POST['mnfacture'], model=request.POST['model'], cpu=request.POST['cpu'], memory=request.POST['memory'], harddisk=request.POST['hardDisk'], is_where=request.POST['where'],
                      is_state=request.POST['state'], purchase_date=request.POST['purchase_date'], comments=request.POST['comments'], member_name_id=request.POST['memberId'], serial=request.POST['serial'])
        asset.save()
        return redirect("assets_main")
    else:
        return render(request, 'assets_main/assets.html', {})
