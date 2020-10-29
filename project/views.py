import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Project
from utils.functions import make_response

@login_required
def client_project_lists(request, client_id):
    reports = Project.objects.filter(client_id=client_id).values('id', 'title')
    if reports.exists():
        reports = list(reports)
        return make_response(status=200, content=json.dumps({'success': True, 'reports': reports}))
    else:
        return make_response(status=400, content=json.dumps({'success': False, 'msg': "해당 고객사의 프로젝트가 존재하지 않습니다."}))