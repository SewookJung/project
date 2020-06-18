import json

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

    if request.method == 'POST' and request.FILES['uploadfile']:
        file = request.FILES['uploadfile']
        load_wb = load_workbook(file, data_only=True)
        load_ws = load_wb['Sheet1']
        iter_rows = iter(load_ws.rows)
        next(iter_rows)
        max_rows = load_ws.max_row
        line_num = 1
        
        # excel에 오류가 있는 경우 err_equip_list에 append한다.
        err_equip_list = []

        for row in iter_rows:
            err_dic = {'no': line_num, 'msg': ''}
            if not row[0].value:
                break
           
            print(line_num)
            print(row[0].value)

            clients = Client.objects.values('name', cnt=Count('name')).get(name=row[0].value)
            if clients.cnt == 0:
                err_dic['msg'] = '고객사명을 확인하세요. '
            products = Product.objects.values('name', cnt=Count('name')).get(name=row[2].value)
            if  products.cnt == 0:
                err_dic['msg'] = err_dic['msg'] + '제품명을 확인하세요. '
            product_models = ProductModel.objects.values('id', cnt=Count('id')).get(name=row[3].value)
            product_model_id = 0

            if product_models.cnt == 0:
                err_dic['msg'] = err_dic['msg'] + '모델명을 확인하세요. '
            else:
                product_model_id = product_models.id

            if Equipment.objects.filter(product_model=product_model_id, serial=row[4].value).count() > 0:
                err_dic['msg'] = err_dic['msg'] + '기존 입력된 동일 모델의 serial이 있습니다.'

            if err_dic['msg'] != '':
                err_equip_list.append(err_dic)

            line_num = line_num + 1
    else:
        err_equip_list.append({'no':1, 'msg': '입력된 파일을 확인하세요'})
    print(err_equip_list)
    return render(request, 'equipment/equipment_upload_check.html', {'err_equip_list' : err_equip_list})


@login_required
@csrf_exempt
def equipment_upload_complete(request):
    # upload complete
    return 'aaaa'

def equipment_upload_cancel(request):
    # upload cancel
    return 'bbbbb'

