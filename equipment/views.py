import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from openpyxl import load_workbook

from .models import EquipmentAttachment, Equipment
from common.models import Client, Product, ProductModel, Mnfacture

from utils.functions import (
    make_response,
)

@login_required
def equipment_main(request):
    equipments = Equipment.objects.all()
    print(equipments)
    return render(request, 'equipment/equipment_main.html', {'equipments': equipments})

@login_required
def equipment_form(request):
    # 1개씩 제품 등록을 하는 경우에 사용하는 폼
    return render(request, 'equipment/equipment_main.html', {})

@login_required
def equipment_input(request):
    # 상품 입력
    return render(request, 'equipment/equipment_main.html', {})
    
@login_required
def equipment_bulk(request):
    return render(request, 'equipment/equipment_bulk.html', {})

@login_required
def equipment_bulk_check(request):
    # 입력된 고객 확인, 장비명확인, 동일 Serial 여부 확인
    return render(request, 'equipment/equipment_bulk.html', {})


@login_required
@csrf_exempt
def equipment_check(request):
    if request.method == "POST":
        file = request.FILES['qqfile']
        load_wb = load_workbook(file, data_only=True)
        load_ws = load_wb['Sheet1']
        iter_rows = iter(load_ws.rows)
        next(iter_rows)
        max_rows = load_ws.max_row
        count = 1
        err_count = 0
        for row in iter_rows:
            try:
                client = Client.objects.get(name=row[0].value)
                product = Product.objects.get(name=row[2].value)
                mnfacture = Mnfacture.objects.get(manafacture=row[1].value)
                product_model = ProductModel.objects.get(name=row[3].value)
                equipment = Equipment(client=client, product=product, mnfacture=mnfacture, product_model=product_model,
                                      serial=row[5].value, location=row[6].value, install_member=row[7].value, install_date=row[8].value, comments=row[9].value)
                equipment.save()
                count += 1
                if count == max_rows-1:
                    equipment_attach_apply = EquipmentAttachment(
                        attach=request.FILES['qqfile'], member_id=request.session['id'], attach_name=request.POST['qqfilename'], content_type=request.FILES['qqfile'].content_type, content_size=request.FILES['qqfile'].size)
                    equipment_attach_apply.save()
                    return make_response(content=json.dumps({'success': True}))

            except Client.DoesNotExist:
                return make_response(status=400, content=json.dumps({'success': False, 'error': "error message to display"}))

    else:
        render(request, 'equipment/equipment_main.html', {})


@login_required
@csrf_exempt
def equipment_upload(request):
    if request.method == "POST":
        file = request.FILES['qqfile']
        load_wb = load_workbook(file, data_only=True)
        load_ws = load_wb['Sheet1']
        iter_rows = iter(load_ws.rows)
        next(iter_rows)
        max_rows = load_ws.max_row
        count = 1

        for row in iter_rows:
            try:
                client = Client.objects.get(name=row[0].value)
                product = Product.objects.get(name=row[2].value)
                mnfacture = Mnfacture.objects.get(manafacture=row[1].value)
                product_model = ProductModel.objects.get(name=row[3].value)
                equipment = Equipment(client=client, product=product, mnfacture=mnfacture, product_model=product_model,
                                      serial=row[5].value, location=row[6].value, install_member=row[7].value, install_date=row[8].value, comments=row[9].value)
                equipment.save()
                count += 1
                if count == max_rows-1:
                    equipment_attach_apply = EquipmentAttachment(
                        attach=request.FILES['qqfile'], member_id=request.session['id'], attach_name=request.POST['qqfilename'], content_type=request.FILES['qqfile'].content_type, content_size=request.FILES['qqfile'].size)
                    equipment_attach_apply.save()
                    return make_response(content=json.dumps({'success': True}))

            except Client.DoesNotExist:
                return make_response(status=400, content=json.dumps({'success': False, 'error': "error message to display"}))

    else:
        render(request, 'equipment/equipment_main.html', {})
