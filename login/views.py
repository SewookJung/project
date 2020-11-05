import requests
import json
from urllib import parse

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout

from member.models import Member
from utils.functions import make_response
from utils.constant import REPORT_PERMISSION_DEFAULT
from django.conf import settings


def login_main(request):
    if request.method == "GET":
        try:
            if request.session.get("member_id", None) == None:
                msg = ""
                return render(request, "login/login.html", {"message": msg})
            elif request.session['member_dept'] in REPORT_PERMISSION_DEFAULT:
                return redirect('weekly_main')
            else:
                return redirect('assets_main')
        except:
            return redirect('assets_main')
    else:
        return render(request, "login/login.html", {})


def login_process(request):
    if request.method == "POST":
        username = request.POST['memberId']
        password = request.POST['memberPw']
        password = parse.quote(password)
        url = settings.AUTH_URL
        cond = f"username={username}&password={password}"
        auth_url = f"{url}?{cond}"

        response = requests.get(auth_url)
        response_status_code = response.status_code

        if response_status_code != 200:
            return make_response(status=400, content=json.dumps({'success': False, 'msg': "사용자 정보를 가지고 올 수 없습니다.\n관리자에게 문의하세요."}))

        else:
            response_objects = json.loads(response.content)['objects']
            
            if not response_objects:
                return make_response(status=400, content=json.dumps({'success': False, 'msg': "존재하지 않는 ID입니다.\n확인 후 다시 시도해주세요."}))
            
            else:
                valid = response_objects[0]['valid']
                username = response_objects[0]['username']

                if valid == True:
                    member_info = Member.objects.get(
                        member_id=username)
                    request.session['id'] = member_info.id
                    request.session['member_id'] = member_info.member_id
                    request.session['member_name'] = member_info.name
                    request.session['member_dept'] = member_info.dept
                    request.session['member_rank'] = member_info.rank

                    user = authenticate(request, username=username)
                    login(request, user)

                    if request.session['member_dept'] in REPORT_PERMISSION_DEFAULT:
                        redirect_url = "/weekly/"
                    else:
                        redirect_url = "/assets/"

                    return make_response(status=200, content=json.dumps({'success': True, 'redirect_url': redirect_url}))
                else:
                    return make_response(status=400, content=json.dumps({'success': False, 'msg': "패스워드가 정확하지 않습니다.\n확인 후 다시 시도하여주세요."}))


def logout_process(request):
    if request.method == "GET":
        if request.session.get("member_id", None) == None:
            return redirect("login_main")
        else:
            try:
                logout(request)
                return redirect("login_main")
            except KeyError:
                return redirect("login_main")
            return redirect("login_main")
    else:
        return redirect("login_main")


def redirect_root(request):
    return redirect('login_main')
