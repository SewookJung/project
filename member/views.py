from django.shortcuts import render

from member.models import Member


def member_profile(request):
    member = Member.objects.get(id=request.session['id'])
    print(member)
    return render(request, "member/member_profile.html", {'member': member})
