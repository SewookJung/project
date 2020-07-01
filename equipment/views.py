import json
from collections import Counter

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from openpyxl import load_workbook
from django.db.models import Count


from .models import EquipmentAttachment, Equipment
from common.models import Client, Product, ProductModel, Mnfacture
from .forms import EquipmentForm

from utils.functions import (
    make_response,
)


@login_required
def equipment_main(request):
    equipments = Equipment.objects.all()
    return render(request, 'equipment/equipment_main.html', {'equipments': equipments})


@login_required
def equipment_form(request):
    equipment_form = EquipmentForm()
    products = Product.objects.values('id',
                                      'name', 'makers', 'level').order_by('makers', 'level')
    return render(request, 'equipment/equipment_form.html', {"products": products, "equipment_form": equipment_form, })


@login_required
def equipment_form_apply(request):
    if request.method == "POST":
        try:
            client = request.POST['client']
            product = request.POST['product_id']
            mnfacture = request.POST['mnfacture']
            product_model = request.POST['product_model']
            serial = request.POST['serial']
            manager = request.POST['manager']
            location = request.POST['location']
            install_date = request.POST['install-date']
            comments = request.POST['comments']

            equipment = Equipment.objects.get(serial=serial)
            raise

        except Equipment.DoesNotExist:
            equipment = Equipment(client_id=client, product_id=product, product_model_id=product_model, serial=serial, mnfacture_id=mnfacture,
                                  manager=manager, location=location, install_date=install_date, comments=comments, creator_id=request.session['id'])
            equipment.save()
            return make_response(status=200, content=json.dumps({'success': True, 'msg': "제품등록에 성공하였습니다."}))

        except:
            return make_response(status=400, content=json.dumps({'success': False, 'msg': "이미 등록되어 있는 serial입니다.\n 확인 후 다시 입력하시기 바랍니다.", 'error': 'serial_error'}))
    else:
        return make_response(status=400, content=json.dumps({'success': False, 'msg': "제품등록 페이지에 다시 접속해주시기 바랍니다.", 'error': 'upload_error'}))


@login_required
def equipment_detail_apply(request, equipment_id):
    if request.method == "POST":
        client = request.POST['client']
        product = request.POST['product_id']
        mnfacture = request.POST['mnfacture']
        product_model = request.POST['product_model']
        manager = request.POST['manager']
        serial = request.POST['serial']
        location = request.POST['location']
        install_date = request.POST['install-date']
        comments = request.POST['comments']
        creator = request.session['id']

        try:
            equipment = Equipment.objects.get(serial=serial)
            raise

        except Equipment.DoesNotExist:
            try:
                modify_equipment = Equipment.objects.get(id=int(equipment_id))
                modify_equipment.client_id = client
                modify_equipment.product_id = product
                modify_equipment.mnfactureauclf_id = mnfacture
                modify_equipment.product_model_id = product_model
                modify_equipment.manager_id = manager
                modify_equipment.serial = serial
                modify_equipment.location = location
                modify_equipment.install_date = install_date
                modify_equipment.comments = comments
                modify_equipment.save()
                return make_response(status=200, content=json.dumps({'success': True, 'msg': "제품수정을 완료하였습니다."}))
            except:
                return make_response(status=400, content=json.dumps({'success': False, 'msg': "제품수정에 실패하였습니다. \n다시 시도하시기 바랍니다.", 'error': 'upload_error'}))

        except:
            return make_response(status=400, content=json.dumps({'success': False, 'msg': "작성된 시리얼 번호가 존재합니다. \n시리얼번호 확인 후 다시 시도하시기 바랍니다.", 'error': 'serial_error'}))
    else:
        return make_response(status=400, content=json.dumps({'success': False, 'msg': "제품수정에 실패하였습니다. \n다시 시도하시기 바랍니다.", 'error': 'upload_error'}))


@login_required
def equipment_detail(request, equipment_id):
    if request.method == "GET":
        equipment_form = EquipmentForm()
        products = Product.objects.values('id',
                                          'name', 'makers', 'level').order_by('makers', 'level')
        equipment = Equipment.objects.get(id=equipment_id)
    return render(request, 'equipment/equipment_detail.html', {"equipment": equipment, "products": products, "equipment_form": equipment_form, 'login_id': request.session['id']})


@login_required
def equipment_input(request):
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
        line_num = 2
        err_equip_list = []
        serial_list = []

        try:
            load_ws = load_wb['장비운용현황']
        except:
            err_equip_list.append(
                {'no': '-', 'msg': '시트명을 확인하세요.\n 기본 시트명은 "장비운용현황" 입니다.'})
            return render(request, 'equipment/equipment_upload_check.html', {'err_equip_list': err_equip_list})

        iter_rows = iter(load_ws.rows)
        next(iter_rows)
        max_rows = load_ws.max_row

        for row in iter_rows:
            client_name = row[0].value
            mnfacture_name = row[1].value
            product_name = row[2].value
            model_name = row[3].value
            serial = row[4].value
            err_dic = {'no': line_num, 'msg': ''}

            try:
                client = Client.objects.get(name=client_name)
            except Client.DoesNotExist:
                err_dic['msg'] = '고객사명을 확인하세요.'

            try:
                mnfacture = Mnfacture.objects.get(manafacture=mnfacture_name)
            except Mnfacture.DoesNotExist:
                err_dic['msg'] = err_dic['msg'] + ' 제조사를 확인하세요.'

            try:
                product = Product.objects.get(name=product_name)
            except Product.DoesNotExist:
                err_dic['msg'] = err_dic['msg'] + ' 제품명을 확인하세요. '

            try:
                product_model = ProductModel.objects.get(name=model_name)
            except ProductModel.DoesNotExist:
                err_dic['msg'] = err_dic['msg'] + ' 모델명을 확인하세요.'

            try:
                equipment = Equipment.objects.get(
                    product_model=product_model.id, serial=serial)
                raise
            except Equipment.DoesNotExist:
                try:
                    serial_list.index(serial)
                    err_dic['msg'] = err_dic['msg'] + \
                        ' 엑셀파일에 중복되는 serail이 있습니다.'
                except ValueError:
                    serial_list.append(serial)
            except:
                err_dic['msg'] = err_dic['msg'] + \
                    ' 기존 입력된 동일 모델의 serial이 있습니다.'

            if len(err_dic['msg']) != 0:
                err_equip_list.append(err_dic)

            line_num = line_num + 1
        if len(err_equip_list) == 0:
            equipment_attach = EquipmentAttachment(member_id=request.session['id'],
                                                   attach=file, attach_name=file.name, content_size=file.size, content_type=file.content_type)
            equipment_attach.save()
        else:
            return render(request, 'equipment/equipment_upload_check.html', {'err_equip_list': err_equip_list})

    else:
        err_equip_list.append({'no': 1, 'msg': '입력된 파일을 확인하세요'})
    return render(request, 'equipment/equipment_upload_check.html', {'err_equip_list': err_equip_list, 'equipment_attach_id': equipment_attach.id})


@login_required
@csrf_exempt
def equipment_upload_complete(request):
    client_objects = Client.objects.all()
    mnfacture_objects = Mnfacture.objects.all()
    product_objects = Product.objects.all()
    product_model_objects = ProductModel.objects.all()
    equipment_attach_id = request.POST['equipment-attach-id']

    equipment_attach = EquipmentAttachment.objects.get(id=equipment_attach_id)
    load_wb = load_workbook(equipment_attach.attach, data_only=True)
    load_ws = load_wb['장비운용현황']
    iter_rows = iter(load_ws.rows)
    next(iter_rows)

    all_values = []
    for row in iter_rows:
        cell_values = []
        for cell in row:
            cell_values.append(cell.value)
        all_values.append(cell_values)

    for item in all_values:
        client = client_objects.values('id').get(name=item[0])
        mnfacture = mnfacture_objects.values('id').get(manafacture=item[1])
        product = product_objects.values('id').get(name=item[2])
        product_model = product_model_objects.values('id').get(name=item[3])
        serial = item[4]
        location = item[5]
        manager = item[6]
        install_date = item[7]

        if item[8] == None:
            comments = ""
        else:
            comments = item[8]

        equipment = Equipment(client_id=client['id'], product_id=product['id'], product_model_id=product_model['id'], mnfacture_id=mnfacture['id'],
                              serial=serial, location=location, manager=manager, install_date=install_date, comments=comments, creator_id=request.session['id'])
        equipment.save()

    return redirect("equipment_main")


def equipment_upload_cancel(request):
    if request.method == 'POST':
        equipment_attach_id = request.POST['equipment_attach_id']
        try:
            EquipmentAttachment.objects.get(id=equipment_attach_id).delete()
            return make_response(status=200, content=json.dumps({'success': True, 'msg': "장비현황 등록을 취소하였습니다."}))
        except:
            return make_response(status=400, content=json.dumps({'success': False, 'error': "장비현황 등록을 취소하는데 실패하였습니다. \n 파일을 다시 업로드 해주시길 바랍니다."}))
    else:
        return make_response(status=400, content=json.dumps({'success': False, 'error': "장비현황 등록을 취소하는데 실패하였습니다. \n 파일을 다시 업로드 해주시길 바랍니다."}))


def equipment_delete(request, equipment_id):
    if request.method == 'GET':
        try:
            Equipment.objects.get(id=equipment_id).delete()
            return make_response(status=200, content=json.dumps({'success': True, 'msg': "해당 제품정보를 삭제하였습니다."}))
        except:
            return make_response(status=400, content=json.dumps({'success': True, 'msg': "해당 제품정보를 삭제하는데 실패 하였습니다."}))
    else:
        return make_response(status=400, content=json.dumps({'success': True, 'msg': "해당 제품정보를 삭제하는데 실패 하였습니다."}))
