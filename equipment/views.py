import json
from collections import Counter

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from openpyxl import load_workbook
from django.db.models import Count


from .models import EquipmentAttachment, Equipment
from common.models import Client, Product, ProductModel, Mnfacture

from utils.functions import (
    make_response,
)


@login_required
def equipment_main(request):
    equipments = Equipment.objects.all()
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
def equipment_upload(request):
    return render(request, 'equipment/equipment_upload.html', {})


@login_required
@csrf_exempt
def equipment_upload_check(request):
    # excel에 오류가 있는 경우 err_equip_list에 append한다.
    if request.method == 'POST' and request.FILES['uploadfile']:
        file = request.FILES['uploadfile']
        load_wb = load_workbook(file, data_only=True)
        load_ws = load_wb['Sheet1']

        iter_rows = iter(load_ws.rows)
        next(iter_rows)

        max_rows = load_ws.max_row
        line_num = 2

        err_equip_list = []
        err_serial_list = []
        serial_list = []

        for row in iter_rows:
            client_name = row[0].value
            mnfacture_name = row[1].value
            product_name = row[2].value
            model_name = row[3].value
            serial = row[5].value

            err_dic = {'no': line_num, 'msg': ''}

            if not client_name:
                err_dic['msg'] = '고객사 이름이 존재하지 않습니다.'
                break

            try:
                client = Client.objects.get(name=client_name)

            except Client.DoesNotExist:
                err_dic['msg'] = '고객사명을 확인하세요.'
                err_equip_list.append(err_dic)

            try:
                mnfacture = Mnfacture.objects.get(manafacture=mnfacture_name)

            except Mnfacture.DoesNotExist:
                err_dic['msg'] = '제조사를 확인하세요.'
                err_equip_list.append(err_dic)

            try:
                product = Product.objects.get(name=product_name)

            except Product.DoesNotExist:
                err_dic['msg'] = '제품명을 확인하세요. '
                err_equip_list.append(err_dic)

            try:
                product_model = ProductModel.objects.get(name=model_name)

            except ProductModel.DoesNotExist:
                err_dic['msg'] = '모델명을 확인하세요.'
                err_equip_list.append(err_dic)

            try:
                equipment = Equipment.objects.get(
                    product_model=product_model.id, serial=serial)
                raise

            except Equipment.DoesNotExist:
                serial_list.append(serial)

            except:
                err_dic['msg'] = '기존 입력된 동일 모델의 serial이 있습니다.'
                err_equip_list.append(err_dic)

            line_num = line_num + 1

        serial_obj = dict(Counter(serial_list))
        for key, value in list(serial_obj.items()):
            if value < 2:
                del serial_obj[key]
        err_serial_list.append(serial_obj)

        if len(err_equip_list) == 0 and len(err_serial_list) == 0:
            equipment_attach = EquipmentAttachment(member_id=request.session['id'],
                                                   attach=file, attach_name=file.name, content_size=file.size, content_type=file.content_type)
            equipment_attach.save()
        else:
            return render(request, 'equipment/equipment_upload_check.html', {'err_equip_list': err_equip_list, 'err_serial_list': err_serial_list})

    else:
        err_equip_list.append({'no': 1, 'msg': '입력된 파일을 확인하세요'})
    return render(request, 'equipment/equipment_upload_check.html', {'err_equip_list': err_equip_list, 'equipment_attach_id': equipment_attach.id})


@login_required
@csrf_exempt
def equipment_upload_complete(request):
    equipment_attach_id = request.POST['equipment-attach-id']
    equipment_attach = EquipmentAttachment.objects.get(id=equipment_attach_id)
    load_wb = load_workbook(equipment_attach.attach, data_only=True)
    load_ws = load_wb['Sheet1']

    iter_rows = iter(load_ws.rows)
    next(iter_rows)

    all_values = []
    for row in iter_rows:
        cell_values = []
        for cell in row:
            cell_values.append(cell.value)
        all_values.append(cell_values)

    print(all_values)

    return render(request, 'equipment/equipment_upload_check.html', {})


def equipment_upload_cancel(request):
    # upload cancel
    return 'bbbbb'
