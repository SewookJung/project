from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from member.models import Member
# Create your views here.


def login(request):
    if request.method == "GET":
        try:
            if request.session.get("member_id", None) == None:
                msg = ""
                return render(request, "login/login.html", {"message": msg})
            else:
                return redirect('assets_main')
        except:
            return redirect('assets_main')
    else:
        return render(request, "login/login.html", {})


def login_process(request):
    if request.method == "POST":
        username = request.POST['member_id']
        password = request.POST['member_pw']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            member_info = Member.objects.get(
                member_id=request.POST['member_id'])
            request.session['id'] = member_info.id
            request.session['member_id'] = member_info.member_id  # 사용자 계정을 저장
            request.session['member_name'] = member_info.name  # 사용자 계정의 이름을 저장
            # 사용자 계정의 부서정보를 저장
            request.session['member_dept'] = member_info.dept
            request.session['member_rank'] = member_info.rank
            auth.login(request, user)
            return redirect("assets_main")
        else:
            msg = "계정 또는 비밀번호가 일치하지 않습니다."
            return render(request, "login/login.html", {"message": msg})
    else:
        msg = "계정 또는 비밀번호가 일치하지 않습니다."
        return render(request, "login/login.html", {"message": msg})


def logout(request):
    if request.method == "GET":
        if request.session.get("member_id", None) == None:
            return redirect("login")
        else:
            try:
                del request.session['member_id']  # 사용자 계정 세션값 삭제
                del request.session['member_name']  # 사용자 이름 삭제
                del request.session['member_dept']  # 사용자 부서값 삭제
                del request.session['member_rank']
                auth.logout(request)
                return redirect("login")
            except KeyError:
                return redirect("login")
            return redirect("login")

    else:
        return redirect("login")


def redirect_root(request):
    return redirect('login')
