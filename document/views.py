import json
import os
import urllib
import uuid
import datetime

from collections import Counter

from django.shortcuts import render, redirect, get_object_or_404, resolve_url, reverse
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core import serializers
from django.core.paginator import Paginator

from wsgiref.util import FileWrapper

from assets.forms import AssetForm
from .forms import DocumentForm
from equipment.forms import EquipmentForm
from .models import Document, DocumentAttachment
from project.models import Project
from member.models import Member
from common.models import Product, Client
from common.views import member_info, member_info_all

from utils.functions import make_response
from utils.constant import REPORT_PERMISSION_DEFAULT

@login_required
def document(request, document_id):
    if request.method == "DELETE":
        try:
            document = Document.objects.get(id=document_id)
            document.delete()
            return make_response(status=200, content=json.dumps({'success': True, 'msg': '문서가 삭제 되었습니다.'}))
        except Document.DoesNotExist:
            return make_response(status=400, content=json.dumps({'success': False, 'msg': '문서가 서버에 존재하지 않습니다.\n관리자에게 문의하세요.'}))
        except:
            return make_response(status=400, content=json.dumps({'success': False, 'msg': '문서를 삭제하는데 실패하였습니다.\n다시 시도해주세요.'}))
    
    if request.method == "PATCH":
        data = QueryDict(request.body)
        modify_object = data['modifyObject']
        try:
            document = Document.objects.get(id=document_id)
            
            if modify_object == "product":
                document.product_id = data['productId']
                document.save()
                msg = "제품명 수정이 완료 되었습니다."
            
            elif modify_object == "category":
                document.category = data['category']
                document.save()
                msg = "구분 수정이 완료 되었습니다."
            return make_response(status=200, content=json.dumps({'success': True, 'msg': msg, 'client_id': document.client_id, 'modify_object': modify_object}))

        except Document.DoesNotExist:
            return make_response(status=400, content=json.dumps({'success': False, 'msg': '문서가 존재하지 않습니다.\n관리자에게 문의하세요.', 'modify_object': modify_object}))

        except:
            return make_response(status=400, content=json.dumps({'success': False, 'msg': '정보를 수정하는데 실패하였습니다.\n다시 시도해 주세요', 'modify_object': modify_object}))
        
@login_required
def document_main(request):
    clients = Client.objects.all().values("id", "name")
    products = Product.objects.values('id',
                                      'name', 'makers', 'level').order_by('makers', 'level')
    document_form = DocumentForm()
    return render(request, 'document/document_main.html', {'clients': clients, 'products':products, 'document_form': document_form, 'permission': REPORT_PERMISSION_DEFAULT})

@login_required
def document_upload(request):
    document_form = DocumentForm()
    dt = datetime.datetime.now()
    check_code = "{0}-{1}-{2}".format(dt.strftime('%Y%m%d'),
                                      uuid.uuid4().hex, request.session['id'])
    products = Product.objects.values('id',
                                      'name', 'makers', 'level').order_by('makers', 'level')
    return render(request, "document/document_upload.html", {'document_form': document_form,  'check_code': check_code, 'products': products, 'permission': REPORT_PERMISSION_DEFAULT})    

#API functions
@login_required
@csrf_exempt
def document_upload_apply(request):
    attach=request.FILES['qqfile']
    attach_name = request.POST['qqfilename']
    category = request.POST['category']
    check_code = request.POST['checkCode']
    client = request.POST['client']
    content_size=request.FILES['qqfile'].size
    content_type=request.FILES['qqfile'].content_type
    mnfacture = request.POST['mnfacture']
    project = int(request.POST['project'])
    product = request.POST['product']
    permissions = json.loads(request.POST['permissions'])

    try:
        document = Document(client_id=client, project=project, category=category, auth=permissions, creator_id=request.session['id'], mnfacture_id=mnfacture, product_id=product,
                        attach_name=attach_name, content_size=content_size, content_type=content_type, attach=attach, check_code=check_code)
        document.save()
        return make_response(status=200, content=json.dumps({'success': True, 'msg': '파일 업로드에 성공하였습니다.'}))

    except:
        return make_response(status=400, content=json.dumps({'success': False, 'msg': "문서 등록에 실패하였습니다.\n다시 시도해주시기 바랍니다."}))

@login_required
def document_attach_lists(request, client_id):
    documents = Document.objects.filter(client_id=client_id).order_by('-id')
    if documents.exists():
        data = []
        for document in documents:
            if document.project != 0:
                project = str(Project.objects.get(id=document.project))
            else:
                project = 0
            created_at = (document.created_at).strftime('%Y-%m-%d')
            product = str(document.product)
            result = {'id': document.id, 'category':document.get_category_display(), 'creator': str(document.creator), 'attach_name': document.attach_name, 'created_at': created_at, 'project': project, 'product': product, 'login_member_name': request.session['member_name']}
            data.append(result)
        return make_response(status=200, content=json.dumps({'success': True, 'data': data}))
    else:
        return make_response(status=400, content=json.dumps({'success': False, 'msg': "해당 고객사의 프로젝트가 존재하지 않습니다."}))

@login_required
@csrf_exempt
def document_download(request, document_id):
    attach_info = Document.objects.get(id=document_id)
    filename = os.path.join(settings.MEDIA_ROOT, attach_info.attach.name)
    response = ""

    if not os.path.exists(settings.MEDIA_ROOT):
        return make_response(status=400, content=json.dumps({'success': False, 'msg': "NAS서버와 연결이 해제되어 파일 업로드가 불가능합니다.\n관리자에게 문의 바랍니다."}))

    if not os.path.exists(filename): 
        return make_response(status=400, content=json.dumps({'success': False, 'msg': "해당 문서가 서버에 존재하지 않아 다운로드 할 수 없습니다.\n관리자에게 문의 바랍니다."}))
    else:
        with open(filename, 'rb') as f:
            response = HttpResponse(FileWrapper(
                f), content_type=attach_info.attach)
            response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'%s' % urllib.parse.quote(
                attach_info.attach_name.encode('utf-8'))
        return response


@login_required
def sites_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    asset_form = AssetForm()
    project_form = ProjectForm()
    document_form = DocumentAttachmentForm()
    products = Product.objects.values(
        'id', 'name', 'makers', 'level').order_by('makers', 'level')
    project_creator = Member.objects.get(id=project.member_id)
    return render(request, 'sites/sites_detail.html', {"project": project, "asset_form": asset_form, "project_form": project_form,  "document_form": document_form, "products": products, "project_creator": project_creator.id, 'login_id': request.session['id'], 'permission': REPORT_PERMISSION_DEFAULT})


@login_required
def sites_edit(request, pk):
    if request.method == "POST":
        try:
            project = Project.objects.get(pk=pk)
            project.title = request.POST['project_name']
            project.status = request.POST['status']
            project.comments = request.POST['sites_comments']
            project.client_id = request.POST['client']
            project.product_id = request.POST['product']
            project.info['sales'] = request.POST['sales_id']
            project.info['mn_cycle'] = request.POST['cycle']
            project.info['eng'] = request.POST['eng']
            project.info['started_at'] = request.POST.getlist('purchase_date')[
                0]
            project.info['ended_at'] = request.POST.getlist('purchase_date')[
                1]
            project.info['mnstarted_at'] = request.POST.getlist('purchase_date')[
                2]
            project.info['mnended_at'] = request.POST.getlist('purchase_date')[
                3]
            project.save()
            return redirect("sites_main")
        except:
            return redirect("sites_main")
    else:
        return redirect("sites_main")


@login_required
def sites_add(request):
    asset_form = AssetForm()
    project_form = ProjectForm()
    document_form = DocumentAttachmentForm()
    products = Product.objects.values('id',
                                      'name', 'makers', 'level').order_by('makers', 'level')
    return render(request, "sites/sites_add.html", {'asset_form': asset_form, 'project_form': project_form, 'document_form': document_form, "products": products, 'permission': REPORT_PERMISSION_DEFAULT})


@login_required
def sites_add_apply(request):
    if request.method == "POST":
        project_apply = Project(title=request.POST['project_name'], status=request.POST['status'],
                                comments=request.POST['sites_comments'], client_id=request.POST[
            'client'], product_id=request.POST['product_id'], member_id=request.session['id'],
            info={"sales": request.POST.getlist('member_name')[0], "mn_cycle": request.POST['cycle'], "eng": request.POST.getlist('member_name')[1], "started_at": request.POST.getlist('purchase_date')[
                0], "ended_at": request.POST.getlist('purchase_date')[1], "mnstarted_at": request.POST.getlist('purchase_date')[2], "mnended_at": request.POST.getlist('purchase_date')[3]}
        )
        project_apply.save()
        return redirect("sites_main")
    else:
        return redirect("sites_main")


@login_required
def sites_delete(request, pk):
    if not os.path.exists(settings.MEDIA_ROOT):
        return make_response(status=400, content=json.dumps({'success': False, 'msg': "NAS서버와 연결이 해제되어 프로젝트 삭제가 불가능합니다.\n관리자에게 문의 바랍니다."}))
    try:
        Project.objects.get(id=pk).delete()
        return make_response(status=200, content=json.dumps({'success': True, 'msg': "프로젝트가 삭제되었습니다."}))
    except:
        return make_response(status=400, content=json.dumps({'success': True, 'msg': "프로젝트를 삭제하는데 실패하였습니다.\n다시 시도해주세요."}))





@login_required
def document_default_auth(request):
    member_info = member_info_all(request)
    selected = {"selected": "true"}
    for item in member_info:
        group_data = item['groupData']
        for item in group_data:
            if item['value'] == request.session['id']:
                item.update(selected)
    return make_response(content=json.dumps({'success': True, 'member_info': member_info, 'permission': REPORT_PERMISSION_DEFAULT}))


@login_required
def document_detail(request, project_id):
    login_id = request.session['id']
    documents = Document.objects.filter(project_id=project_id)
    documents_attach = DocumentAttachment.objects.all()
    documents_id = documents.values("id")
    project_name = documents[0].project
    documents_attach_list = []
    for document_id in documents_id:
        document_attach_list = documents_attach.filter(
            document_id=document_id['id'])
        for attach in document_attach_list:
            document = documents.get(id=attach.document_id)
            document_auth_value = [item['value'] for item in document.auth]
            document_auth_value.append(str(document.member_id))
            rework_document_attached = {'id': attach.id, 'attach_name': attach.attach_name, 'document_id': attach.document_id,
                                        'created_at': attach.created_at, 'permission': document.auth, 'kind': document.kind, 'member': document.member, 'auth_value': document_auth_value}
            documents_attach_list.append(rework_document_attached)
    return render(request, "sites/document_detail.html", {"documents_attach_list": documents_attach_list, 'project_name': project_name, 'login_id': login_id, 'permission': REPORT_PERMISSION_DEFAULT})


@login_required
def document_attach_detail(request, document_id):
    document_form = DocumentForm()
    document_all = Document.objects.all()
    document_attach_all = DocumentAttachment.objects.all()
    document = document_all.get(id=document_id)
    document_attach_list = document_attach_all.filter(document=document_id)
    dt = datetime.datetime.now()
    check_code = "{0}-{1}-{2}".format(dt.strftime('%Y%m%d'),
                                      uuid.uuid4().hex, request.session['id'])
    return render(request, "sites/document_attach_detail.html", {'document_form': document_form, 'document': document, 'document_attach_list': document_attach_list, 'check_code': check_code, 'permission': REPORT_PERMISSION_DEFAULT})


@login_required
def document_attach_kind_get_detail(request, project_id):
    kind = request.GET['kind']
    middle_class = request.GET['middleClass']

    if kind == "PRE":
        documents = Document.objects.filter(
            project=project_id, kind=kind, pre_middle_class=middle_class)
    elif kind == "PRO":
        documents = Document.objects.filter(
            project=project_id, kind=kind, pro_middle_class=middle_class)
    elif kind == "EXA":
        documents = Document.objects.filter(
            project=project_id, kind=kind, exa_middle_class=middle_class)
    elif kind == "MAN":
        documents = Document.objects.filter(
            project=project_id, kind=kind, man_middle_class=middle_class)
    else:
        documents = Document.objects.filter(
            project=project_id, kind=kind, etc_middle_class=middle_class)

    document_attach_names = []
    for document in documents:
        document_attachs = DocumentAttachment.objects.filter(
            document=document.id)
        for document_attach in document_attachs:
            document_attach_names.append(document_attach.attach_name)
    return make_response(content=json.dumps({'success': True, 'document_attach_names': document_attach_names, 'permission': REPORT_PERMISSION_DEFAULT}))


@login_required
def document_attach_kind_detail(request, document_id, middle_class, kind):
    login_id = request.session['id']
    document_all = Document.objects.all()
    document_attach_all = DocumentAttachment.objects.all()

    document = document_all.get(id=document_id)

    if kind == "PRE":
        documents_id = document_all.filter(
            project=document.project_id, kind=document.kind, pre_middle_class=middle_class).values('id')
    elif kind == "PRO":
        documents_id = document_all.filter(
            project=document.project_id, kind=document.kind, pro_middle_class=middle_class).values('id')
    elif kind == "EXA":
        documents_id = document_all.filter(
            project=document.project_id, kind=document.kind, exa_middle_class=middle_class).values('id')
    elif kind == "MAN":
        documents_id = document_all.filter(
            project=document.project_id, kind=document.kind, man_middle_class=middle_class).values('id')
    else:
        documents_id = document_all.filter(
            project=document.project_id, kind=document.kind, etc_middle_class=middle_class).values('id')

    project_name = document.project
    documents_attach_list = []
    for document_id in documents_id:
        document_attach_list = document_attach_all.filter(
            document=document_id['id'])
        for attach in document_attach_list:
            document_auth_value = [item['value'] for item in document.auth]
            document_auth_value.append(str(document.member_id))
            rework_document_attached = {'id': attach.id, 'attach_name': attach.attach_name, 'document_id': attach.document_id,
                                        'created_at': attach.created_at, 'permission': document.auth, 'kind': document.kind, 'member': document.member, 'auth_value': document_auth_value}
            documents_attach_list.append(rework_document_attached)
    return render(request, "sites/document_attach_kind_detail.html", {"documents_attach_list": documents_attach_list, 'project_name': project_name, 'login_id': login_id, 'permission': REPORT_PERMISSION_DEFAULT})


@login_required
def document_attach_detail_apply(request, document_id):
    permissions = json.loads(request.POST['permission'])
    kind = request.POST['kind']
    middle_class = request.POST['middleClass']

    document = Document.objects.get(id=document_id)
    document.kind = kind
    document.auth = permissions

    if kind == "PRE":
        document.pre_middle_class = middle_class
    elif kind == "PRO":
        document.pro_middle_class = middle_class
    elif kind == "EXA":
        document.exa_middle_class = middle_class
    elif kind == "MAN":
        document.man_middle_class = middle_class
    else:
        document.etc_middle_class = middle_class
    document.save()
    return make_response(content=json.dumps({'success': True}))


@login_required
@csrf_exempt
def document_attach_detail_upload_apply(request):
    return make_response(content=json.dumps({'success': True}))


@login_required
def document_attach_auth(request, document_id):
    document = Document.objects.get(id=document_id)
    selected = {"selected": "true"}
    document_auth = document.auth
    member_info = member_info_all(request)

    for item in document_auth:
        auth_name = item['name']
        for item in member_info:
            group_data = item['groupData']
            for item in group_data:
                if auth_name == item['name']:
                    item.update(selected)
    return make_response(content=json.dumps({'success': True, 'auth_info': member_info}))








@login_required
@csrf_exempt
def document_reg_delete(request):
    try:
        Document.objects.get(id=int(request.POST['document_id'])).delete()
        return make_response(status=200, content=json.dumps({'success': True}))
    except:
        return make_response(status=400, content=json.dumps({'success': False, 'msg': "문서를 삭제하는데 실패하였습니다."}))


@login_required
def document_delete(request, document_id):
    if not os.path.exists(settings.MEDIA_ROOT):
        return make_response(status=400, content=json.dumps({'success': False, 'msg': "NAS서버와 연결이 해제되어 문서삭제가 불가능합니다.\n관리자에게 문의 바랍니다."}))

    try:
        document_all = Document.objects.all()
        document_all.filter(id=document_id).delete()
        return make_response(status=200, content=json.dumps({'success': True, 'msg': "해당 프로젝트의 모든 문서를 삭제하였습니다."}))
    except:
        return make_response(status=400, content=json.dumps({'success': False, 'msg': "해당 프로젝트의 모든 문서를 삭제하는데 실패하였습니다.\n다시 시도해주시기 바랍니다."}))


@login_required
def document_attach_delete(request, attachment_id):
    if not os.path.exists(settings.MEDIA_ROOT):
        return make_response(status=400, content=json.dumps({'success': False, 'msg': "NAS서버와 연결이 해제되어 문서삭제가 불가능합니다.\n관리자에게 문의 바랍니다."}))

    document_attach_all = DocumentAttachment.objects.all()
    document_id = document_attach_all.values(
        "document_id").get(id=attachment_id)
    attach_count = document_attach_all.filter(
        document_id=document_id['document_id']).count()
    if attach_count > 1:
        DocumentAttachment.objects.get(id=attachment_id).delete()
        return make_response(status=200, content=json.dumps({'success': True, 'isAble': True}))
    else:
        Document.objects.get(id=document_id['document_id']).delete()
        return make_response(status=200, content=json.dumps({'success': True, 'isAble': False}))


@login_required
@csrf_exempt
def document_download_check(request, pk):
    if not os.path.exists(settings.MEDIA_ROOT):
        return make_response(status=400, content=json.dumps({'success': False, 'msg': "NAS서버와 연결이 해제되어 파일 업로드가 불가능합니다.\n관리자에게 문의 바랍니다."}))

    attach_info = DocumentAttachment.objects.get(id=pk)
    filename = os.path.join(settings.MEDIA_ROOT, attach_info.attach.name)

    if not os.path.exists(filename):
        return make_response(status=400, content=json.dumps({'success': False, 'msg': "해당 문서가 서버에 존재하지 않아 다운로드 할 수 없습니다.\n관리자에게 문의 바랍니다."}))


@login_required
def client_reports_test(request, client_id):
    reports = Project.objects.filter(client_id=client_id)
    if reports.exists():
        reports = serializers.serialize('json', reports)
        return make_response(status=200, content=json.dumps({'success': True, 'reports': reports}))
    else:
        return make_response(status=400, content=json.dumps({'success': False, 'msg': "해당 고객사의 문서 업로드를 할 수 있는 리포트가 존재하지 않습니다."}))


@login_required
def document_upload_test(request):
    document_form = DocumentForm()
    project_form = ProjectForm()
    dt = datetime.datetime.now()
    check_code = "{0}-{1}-{2}".format(dt.strftime('%Y%m%d'),
                                      uuid.uuid4().hex, request.session['id'])
    return render(request, "sites/sites_upload_test.html", {'project_form': project_form, 'document_form': document_form,  'check_code': check_code, 'permission': REPORT_PERMISSION_DEFAULT})
