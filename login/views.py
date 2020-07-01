from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth

from member.models import Member
from utils.constant import REPORT_PERMISSION_DEFAULT


def login(request):
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
        try:
            member_id = request.POST['member_id']
            member_pw = request.POST['member_pw']
            member = Member.objects.get(member_id=member_id)
            member_status = member.status

            if member_status == "Passive":
                raise
            else:
                user = auth.authenticate(
                    request, username=member_id, password=member_pw)
                if user is not None:
                    member_info = Member.objects.get(
                        member_id=member_id)
                    request.session['id'] = member_info.id
                    request.session['member_id'] = member_info.member_id
                    request.session['member_name'] = member_info.name
                    request.session['member_dept'] = member_info.dept
                    request.session['member_rank'] = member_info.rank
                    auth.login(request, user)
                    if request.session['member_dept'] in REPORT_PERMISSION_DEFAULT:
                        return redirect("weekly_main")
                    else:
                        return redirect("assets_main")
                else:
                    msg = "계정 또는 비밀번호가 일치하지 않습니다."
                    return render(request, "login/login.html", {"message": msg})

        except Member.DoesNotExist:
            msg = "계정 또는 비밀번호가 일치하지 않습니다."
            return render(request, "login/login.html", {"message": msg})

        except:
            msg = "해당 계정은 비활성화 되었습니다.\n관리자에게 연락하세요"
            return render(request, "login/login.html", {"message": msg})


def logout(request):
    if request.method == "GET":
        if request.session.get("member_id", None) == None:
            return redirect("login")
        else:
            try:
                del request.session['member_id']
                del request.session['member_name']
                del request.session['member_dept']
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
