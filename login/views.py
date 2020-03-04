from django.shortcuts import render, redirect
from django.http import HttpResponse
from member.models import Member
# Create your views here.


def login(request):
    msg = ""
    return render(request, "login/login.html", {"message":msg})


def login_process(request):
    try:
        member_info = Member.objects.get(member_id=request.POST['member_id']) # Member 테이블에서 로그인 계정과 일치하는 데이터를 추출
        if member_info.pw == request.POST['member_pw']: # 사용자가 입력한 비밀번호와 Member 테이블에 등록된 비밀번호가 일치하는 경우
            request.session['member_id'] = member_info.member_id # 사용자 계정을 저장
            request.session['member_name'] = member_info.name # 사용자 계정의 이름을 저장
            request.session['member_dept'] = member_info.dept # 사용자 계정의 부서정보를 저장
            request.session['member_rank'] = member_info.rank
            return redirect('/assets')
        else: # 사용자가 입력한 비밀번호와 Member 테이블에 등록된 비밀번호가 불일치하는 경우 아래의 메시지를 리턴
             msg = "계정 또는 비밀번호가 일치하지 않습니다."
             return render(request, "login/login.html", {"message":msg})
    except Member.DoesNotExist as msg: # DoesNotExist 오류 발생시 아래의 메시지를 리턴
        msg = "계정 또는 비밀번호가 일치하지 않습니다."
        return render(request, "login/login.html", {"message":msg})

def logout(request):
    try:
        del request.session['member_id'] # 사용자 계정 세션값 삭제
        del request.session['member_name'] # 사용자 이름 삭제
        del request.session['member_dept'] # 사용자 부서값 삭제
        del request.session['member_rank'] 
    except KeyError:
        pass
    msg = ""
    return render(request, "login/login.html", {"message":msg})

