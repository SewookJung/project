import json


from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required

from member.models import Member
from .models import Client, Mnfacture, ProductModel, Product
from utils.constant import REPORT_PERMISSION_DEFAULT, SIMILAR_WORD_DEFAULT
from utils.functions import make_response


@login_required
def member_info(request):
    members = Member.objects.all()
    depts = members.values('dept').distinct().order_by('dept')

    members_data = []

    for dept in depts:
        classify_member = members.filter(dept=dept['dept'])
        data_format = {
            'groupName': dept['dept'],
            'groupData': []}

        for member in classify_member:
            data_format['groupData'].append(
                {'name': member.name + " " + member.rank, 'value': member.id})
        members_data.append(data_format)
    return make_response(status=200, content=json.dumps({'members_data': members_data}))


@login_required
def member_info_all(request):
    members = Member.objects.all()
    depts = members.values('dept').distinct().order_by('dept')

    members_data = []

    for dept in depts:
        classify_member = members.filter(dept=dept['dept'])
        data_format = {
            'groupName': dept['dept'],
            'groupData': []}

        for member in classify_member:
            data_format['groupData'].append(
                {'name': member.name + " " + member.rank, 'value': member.id})
        members_data.append(data_format)
    return members_data


@login_required
def weekly_permission(request):
    return render(request, 'common/common_permission.html', {'permission': REPORT_PERMISSION_DEFAULT})


@login_required
def client_dup_check(request):
    try:
        clients = Client.objects.all()
        client_name = request.POST['clientName']
        client = clients.get(name=client_name)

        similar_client_list = []
        similar = clients.values('similar_word', 'name')
        for item in similar:
            if client_name in item['similar_word']['similar']:
                similar_client_list.append(item['name'])

            if client_name in item['name']:
                similar_client_list.append(item['name'])

        return make_response(status=400, content=json.dumps({'success': False, 'client_name': client.name, "similar_client_list": similar_client_list}))

    except Client.DoesNotExist:
        similar_client_list = []
        similar = clients.values('similar_word', 'name')
        for item in similar:
            if client_name in item['similar_word']['similar']:
                similar_client_list.append(item['name'])

            if client_name in item['name']:
                similar_client_list.append(item['name'])

        return make_response(status=200, content=json.dumps({'success': True, "similar_client_list": similar_client_list}))


@login_required
def client_add_apply(request):
    try:
        new_client_name = request.POST['clientName']
        new_client = Client(name=new_client_name,
                            similar_word=SIMILAR_WORD_DEFAULT)
        new_client.save()
        return make_response(status=200, content=json.dumps({'success': True, 'msg': "고객사 신규 등록에 성공하였습니다.", 'test': 'test'}))
    except:
        return make_response(status=400, content=json.dumps({'success': False, 'msg': "고객사 신규 등록에 실패하였습니다.\n다시 시도해주세요."}))


@login_required
def get_mnfacture_id(request, mnfacture):
    try:
        mnfacture_id = Mnfacture.objects.get(manafacture=mnfacture).id
        return make_response(status=200, content=json.dumps({'success': True, 'mnfacture_id': mnfacture_id}))
    except:
        return make_response(status=400, content=json.dumps({'success': False, 'msg': "제조사 정보를 정확히 가지고 오지 못하였습니다.\n다시 시도해주시기 바랍니다."}))


@login_required
def get_model_id(request, model):
    try:
        model = ProductModel.objects.get(name=model)
        model_id = model.id
        mnfacture_id = Product.objects.get(pk=model.product_id.id).mnfacture.id
        return make_response(status=200, content=json.dumps({'success': True, 'model_id': model_id, 'mnfacture_id': mnfacture_id}))
    except:
        return make_response(status=200, content=json.dumps({'success': True, 'msg': "고객사 신규 등록에 성공하였습니다."}))
