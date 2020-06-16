import json

from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from member.models import Member

from utils.functions import make_response


@login_required
def member_profile(request):
    member = Member.objects.get(id=request.session['id'])
    return render(request, "member/member_profile.html", {'member': member})


@login_required
def member_password(request):
    return render(request, "member/member_password.html", {})


@login_required
def member_password_apply(request):
    if request.method == "POST":
        current_password = request.POST.get("origin_password")
        password = request.POST.get('password1')
        user = request.user
        if check_password(current_password, user.password):
            new_password = request.POST.get('password1')
            password_confirm = request.POST.get('password2')
            if len(password) < 8:
                return make_response(status=400, content=json.dumps({'success': False, 'comment': "변경할 비밀번호는 최소 8자리 입니다."}))
            else:
                if new_password == password_confirm:
                    user.set_password(new_password)
                    user.save()
                    auth.login(request, user)
                    member_info = Member.objects.get(member_id=user)
                    request.session['member_id'] = member_info.member_id
                    request.session['member_name'] = member_info.name
                    request.session['member_dept'] = member_info.dept
                    request.session['member_rank'] = member_info.rank
                    return make_response(content=json.dumps({'success': True, 'comment': "비밀번호 변경이 완료 되었습니다."}))
                else:
                    return make_response(status=400, content=json.dumps({'success': False, 'comment': "새로운 비밀번호를 다시 확인해주세요."}))
        else:
            return make_response(status=400, content=json.dumps({'success': False, 'comment': "현재 비밀번호가 일치하지 않습니다. 다시 확인해주세요."}))
