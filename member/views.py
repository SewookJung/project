from django.shortcuts import render

from member.models import Member


def member_profile(request):
    member = Member.objects.get(id=request.session['id'])
    print(member)
    return render(request, "member/member_profile.html", {'member': member})


def member_password(request):
    return render(request, "member/member_password.html", {})


def member_password_apply(request):
    print(request.POST)
    return render(request, "member/member_password.html", {})
