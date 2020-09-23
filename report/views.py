from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from member.models import Member
from common.models import Client, Product

from utils.constant import REPORT_PERMISSION_DEFAULT


@login_required
def report_project(request):
    sales = Member.objects.filter(dept='사업본부')
    engineers = Member.objects.filter(
        Q(dept='기술 1팀') |
        Q(dept='기술 2팀') |
        Q(dept='남부팀')
    )
    return render(request, 'report/report_project.html', {'sales': sales, 'engineers': engineers, 'permission': REPORT_PERMISSION_DEFAULT})


@login_required
def report_dashboard(request):
    return render(request, 'report/report_dashboard.html', {'permission': REPORT_PERMISSION_DEFAULT})


@login_required
def report_project_dashboard(request):
    return render(request, 'report/report_project_dashboard.html', {'permission': REPORT_PERMISSION_DEFAULT})


@login_required
def report_project_edit(request):
    return render(request, 'report/report_project_edit.html', {'permission': REPORT_PERMISSION_DEFAULT})


@login_required
def report_maintenance(request):
    return render(request, 'report/report_maintenance.html', {'permission': REPORT_PERMISSION_DEFAULT})


@login_required
def report_maintenance_dashboard(request):
    return render(request, 'report/report_maintenance_dashboard.html', {'permission': REPORT_PERMISSION_DEFAULT})


@login_required
def report_maintenance_client(request):
    return render(request, 'report/report_maintenance_client.html', {'permission': REPORT_PERMISSION_DEFAULT})


@login_required
def report_maintenance_client_detail(request):
    return render(request, 'report/report_maintenance_client_detail.html', {'permission': REPORT_PERMISSION_DEFAULT})


@login_required
def report_support(request):
    sales = Member.objects.filter(dept='사업본부')
    engineers = Member.objects.filter(
        Q(dept='기술 1팀') |
        Q(dept='기술 2팀') |
        Q(dept='남부팀')
    )
    clients = Client.objects.all()
    products = Product.objects.values(
        'id', 'name', 'makers', 'level').order_by('makers', 'level')
    return render(request, 'report/report_support.html', {'sales': sales, 'engineers': engineers, 'clients': clients, 'products': products, 'permission': REPORT_PERMISSION_DEFAULT})


@login_required
def report_support_detail(request):
    return render(request, 'report/report_support_detail.html', {'permission': REPORT_PERMISSION_DEFAULT})


@login_required
def report_edu(request):
    clients = Client.objects.all()
    products = Product.objects.values(
        'id', 'name', 'makers', 'level').order_by('makers', 'level')
    return render(request, 'report/report_edu.html', {'clients': clients, 'products': products, 'permission': REPORT_PERMISSION_DEFAULT})


@login_required
def report_edu_detail(request):
    return render(request, 'report/report_edu_detail.html', {'permission': REPORT_PERMISSION_DEFAULT})


@login_required
def report_etc(request):
    clients = Client.objects.all()
    products = Product.objects.values(
        'id', 'name', 'makers', 'level').order_by('makers', 'level')
    return render(request, 'report/report_etc.html', {'clients': clients, 'products': products, 'permission': REPORT_PERMISSION_DEFAULT})


@login_required
def report_etc_detail(request):
    return render(request, 'report/report_etc_detail.html', {'permission': REPORT_PERMISSION_DEFAULT})
