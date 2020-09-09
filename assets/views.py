from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from datetime import datetime

from assets.models import Asset, Assetrent
from .forms import AssetForm, AssetrentForm
from utils.constant import ASSET_STATUS_PERSONAL, ASSET_STATUS_TEST, ASSET_STATUS_RENTAL, ASSET_STATUS_DISPOSAL, ASSET_STATUS_KEEP, REPORT_PERMISSION_DEFAULT


@login_required
def assets_main(request):
    assets = Asset.objects.exclude(
        is_state=ASSET_STATUS_RENTAL) & Asset.objects.exclude(is_state=ASSET_STATUS_DISPOSAL) & Asset.objects.exclude(is_state=ASSET_STATUS_KEEP)
    return render(request, 'assets_main/assets_main.html', {'assets': assets, 'permission': REPORT_PERMISSION_DEFAULT})


@login_required
def assets_add(request):
    form = AssetForm()
    return render(request, 'assets_main/assets_add.html', {'form': form, 'permission': REPORT_PERMISSION_DEFAULT})


@login_required
def assets_status(request):
    assets = Asset.objects.filter(
        Q(is_state=ASSET_STATUS_RENTAL) |
        Q(is_state=ASSET_STATUS_KEEP)
    )
    rent_form = AssetForm()
    return render(request, 'assets_main/assets_status.html', {'assets': assets, 'rent_form': rent_form, 'ASSET_STATUS_RENTAL': ASSET_STATUS_RENTAL, 'permission': REPORT_PERMISSION_DEFAULT})


@login_required
def assets_rent(request):
    if request.method == "POST":
        asset = Asset.objects.get(pk=request.POST['assetId'])
        asset.is_state = ASSET_STATUS_RENTAL
        asset.save()
        asset_rent = Assetrent(stdate=request.POST['stDate'], eddate=request.POST['edDate'],
                               comments=request.POST['comments'], asset_id=request.POST['assetId'], member_name=request.POST['memberName'])
        asset_rent.save()
        return redirect('assets_status')
    else:
        return render(request, 'assets_main/assets_rent.html', {'permission': REPORT_PERMISSION_DEFAULT})


@login_required
def assets_return(request):
    if request.method == "POST":
        asset_rent = Assetrent.objects.get(
            id=request.POST['assetrentId'])
        asset_rent.return_date = datetime.now()
        asset_rent.save()
        asset = Asset.objects.get(pk=request.POST['assetId'])
        asset.is_state = ASSET_STATUS_KEEP
        asset.is_where = "본사"
        asset.save()
        return redirect('assets_status')
    else:
        return render(request, 'assets_main/assets_status.html', {'permission': REPORT_PERMISSION_DEFAULT})


@login_required
def assets_add_apply(request):
    if request.method == "POST":
        asset = Asset(mnfacture=request.POST['mnfacture'], model=request.POST['model'], cpu=request.POST['cpu'], memory=request.POST['memory'], harddisk=request.POST['hardDisk'], is_where=request.POST['where'],
                      is_state=request.POST['state'], purchase_date=request.POST['purchase_date'], comments=request.POST['comments'], member_name_id=request.POST['memberId'], serial=request.POST['serial'])
        asset.save()
        asset_status = int(request.POST['state'])
        if asset_status == ASSET_STATUS_RENTAL:
            asset_rent = Assetrent(stdate=request.POST['rentDate'], eddate=request.POST['returnDate'],
                                   comments=request.POST['comments'], asset_id=asset.id, member_name=request.POST['memberName'])
            asset_rent.save()
        return redirect("assets_main")
    else:
        return render(request, 'assets_main/assets.html', {'permission': REPORT_PERMISSION_DEFAULT})
