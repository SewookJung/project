from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from datetime import datetime
from assets.models import Asset, Assetrent
from .forms import AssetForm, AssetrentForm
from django.contrib.auth.decorators import login_required


@login_required
def assets_main(request):
    assets = Asset.objects.exclude(
        is_state=4) & Asset.objects.exclude(is_state=5) & Asset.objects.exclude(is_state=3)
    return render(request, 'assets_main/assets_main.html', {'assets': assets})


@login_required
def assets_add(request):
    form = AssetForm()
    return render(request, 'assets_main/assets_add.html', {'form': form})


@login_required
def assets_status(request):
    assets = Asset.objects.filter(
        Q(is_state=3) |
        Q(is_state=5)
    )
    rent_form = AssetForm()
    return render(request, 'assets_main/assets_status.html', {'assets': assets, 'rent_form': rent_form, })


@login_required
def assets_rent(request):
    if request.method == "POST":
        asset = Asset.objects.get(pk=request.POST['assetId'])
        asset.is_state = 3
        asset.save()
        asset_rent = Assetrent(stdate=request.POST['stDate'], eddate=request.POST['edDate'],
                               comments=request.POST['comments'], asset_id=request.POST['assetId'], member_name=request.POST['memberName'])
        asset_rent.save()
        return redirect('assets_status')
    else:
        return render(request, 'assets_main/assets_rent.html', {})


@login_required
def assets_return(request):
    if request.method == "POST":
        asset_rent = Assetrent.objects.get(
            id=request.POST['assetrentId'])
        asset_rent.return_date = datetime.now()
        asset_rent.save()
        asset = Asset.objects.get(pk=request.POST['assetId'])
        asset.is_state = 5
        asset.is_where = "본사"
        asset.save()
        return redirect('assets_status')
    else:
        return render(request, 'assets_main/assets_status.html', {})


@login_required
def assets_add_apply(request):
    if request.method == "POST":
        asset = Asset(mnfacture=request.POST['mnfacture'], model=request.POST['model'], cpu=request.POST['cpu'], memory=request.POST['memory'], harddisk=request.POST['hardDisk'], is_where=request.POST['where'],
                      is_state=request.POST['state'], purchase_date=request.POST['purchase_date'], comments=request.POST['comments'], member_name_id=request.POST['memberId'], serial=request.POST['serial'])
        asset.save()
        return redirect("assets_main")
    else:
        return render(request, 'assets_main/assets.html', {})
