import json


from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required

from member.models import Member
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
