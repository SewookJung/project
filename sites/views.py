import json
import os
import urllib
import uuid
import datetime
from collections import Counter

from django.shortcuts import render, redirect, get_object_or_404, resolve_url, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.paginator import Paginator

from wsgiref.util import FileWrapper

from assets.forms import AssetForm
from .forms import ProjectForm, DocumentAttachmentForm, DocumentForm
from .models import Document, DocumentAttachment, Project
from member.models import Member
from common.models import Product
from common.views import member_info, member_info_all

from utils.functions import make_response
from utils.constant import REPORT_PERMISSION_DEFAULT


@login_required
def sites_main_test(request):
    documents = Document.objects
    document_list = Document.objects.all()
    paginator = Paginator(document_list, 3)
    page = request.GET.get('page', 1)
    posts = paginator.get_page(page)
    print(posts)
    return render(request, 'sites/sites_main_test.html', {'documents': documents, 'posts': posts, 'permission': REPORT_PERMISSION_DEFAULT})


@login_required
def sites_main(request):
    projects = Project.objects.all()
    documents_all = Document.objects.all()

    project_lists = []
    for project in projects:

        rework_reports = {'id': project.id, 'client': project.client, 'product': project.product, 'creator': project.member, 'document_id': None,
                          'title': project.title, 'PRE': {}, "PRO": {}, "EXA": {}, "MAN": {}, "ETC": {}, }
        documents = documents_all.filter(
            project=project.id).order_by('project')

        for document in documents:
            document_attachs = DocumentAttachment.objects.filter(
                document=document.id)
            kind = document.kind
            count = document_attachs.count()

            if kind == "PRE":
                middle_class = document.pre_middle_class
                if rework_reports['PRE'].get(middle_class) == None:
                    data = {
                        middle_class: {
                            'document_id': document.id,
                            'count': count
                        }
                    }
                    rework_reports['PRE'].update(data)
                else:
                    add_count = rework_reports['PRE'][middle_class]['count'] + count
                    rework_reports['PRE'][middle_class]['count'] = add_count

            elif kind == "PRO":
                middle_class = document.pro_middle_class
                if rework_reports['PRO'].get(middle_class) == None:
                    data = {
                        middle_class: {
                            'document_id': document.id,
                            'count': count
                        }
                    }
                    rework_reports['PRO'].update(data)
                else:
                    add_count = rework_reports['PRO'][middle_class]['count'] + count
                    rework_reports['PRO'][middle_class]['count'] = add_count

            elif kind == "EXA":
                middle_class = document.exa_middle_class
                if rework_reports['EXA'].get(middle_class) == None:
                    data = {
                        middle_class: {
                            'document_id': document.id,
                            'count': count
                        }
                    }
                    rework_reports['EXA'].update(data)
                else:
                    add_count = rework_reports['EXA'][middle_class]['count'] + count
                    rework_reports['EXA'][middle_class]['count'] = add_count

            elif kind == "MAN":
                middle_class = document.man_middle_class
                if rework_reports['MAN'].get(middle_class) == None:
                    data = {
                        middle_class: {
                            'document_id': document.id,
                            'count': count
                        }
                    }
                    rework_reports['MAN'].update(data)
                else:
                    add_count = rework_reports['MAN'][middle_class]['count'] + count
                    rework_reports['MAN'][middle_class]['count'] = add_count

            else:
                middle_class = document.etc_middle_class
                if rework_reports['ETC'].get(middle_class) == None:
                    data = {
                        middle_class: {
                            'document_id': document.id,
                            'count': count
                        }
                    }
                    rework_reports['ETC'].update(data)
                else:
                    add_count = rework_reports['ETC'][middle_class]['count'] + count
                    rework_reports['ETC'][middle_class]['count'] = add_count

            document_id = {'document_id': document.id}
            rework_reports.update(document_id)
        project_lists.append(rework_reports)
    return render(request, 'sites/sites_main.html', {"projects": project_lists, 'permission': REPORT_PERMISSION_DEFAULT})


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
    Project.objects.get(id=pk).delete()
    return redirect("sites_main")


@login_required
def document_upload(request):
    document_form = DocumentForm()
    dt = datetime.datetime.now()
    check_code = "{0}-{1}-{2}".format(dt.strftime('%Y%m%d'),
                                      uuid.uuid4().hex, request.session['id'])
    return render(request, "sites/sites_upload.html", {'document_form': document_form,  'check_code': check_code, 'permission': REPORT_PERMISSION_DEFAULT})


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
    document.kind = request.POST['kind']
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
def document_reg_apply(request):
    permission = json.loads(request.POST['permission'])
    middle_class = request.POST['middleClass']
    kind = request.POST['kind']
    try:
        document_apply = Document(
            project_id=request.POST['project'], member_id=request.session[
                'id'], kind=request.POST['kind'], auth=permission,
        )
        if kind == "PRE":
            document_apply.pre_middle_class = middle_class
        elif kind == "PRO":
            document_apply.pro_middle_class = middle_class
        elif kind == "EXA":
            document_apply.exa_middle_class = middle_class
        elif kind == "MAN":
            document_apply.man_middle_class = middle_class
        else:
            document_apply.etc_middle_class = middle_class
        document_apply.save()
        return make_response(content=json.dumps({'success': True, 'document_id': document_apply.id}))
    except:
        return make_response(status=400, content=json.dumps({'success': False, 'error': "document save error"}))


@login_required
@csrf_exempt
def document_upload_apply(request):
    """
       1) check_code가 있는지 확인한다.
       2) check_code로 documentattach에 입력된 정보가 있는지 확인한다.
       3) check_code가 입력된 docuemntattach가 있는 경우 document_id를 가지고 온다.
          없는 경우 신규 입력 처리한다.
    """
    if not request.POST['document_id'] == "":
        try:
            if not os.path.exists(settings.MEDIA_ROOT):
                return make_response(status=400, content=json.dumps({'success': False, 'error': "NAS서버와 연결이 해제되어 파일 업로드가 불가능합니다.\n관리자에게 문의 바랍니다."}))

            document_attach_apply = DocumentAttachment(
                attach_name=request.POST['qqfilename'], content_size=request.FILES[
                    'qqfile'].size, content_type=request.FILES['qqfile'].content_type,
                document_id=request.POST['document_id'], attach=request.FILES['qqfile'], check_code=request.POST['check_code']
            )
            document_attach_apply.save()
            return make_response(content=json.dumps({'success': True, }))
        except:
            return make_response(status=400, content=json.dumps({'success': False, 'error': "파일 업로드에 실패하였습니다. 다시 시도하여주세요."}))
    else:
        return make_response(status=400, content=json.dumps({'success': False, 'error': "파일 업로드에 실패하였습니다. 다시 시도하여주세요."}))


@login_required
@csrf_exempt
def document_reg_delete(request):
    # 파일업로드 과정에서 실패한 경우 신규의 경우 document삭제 및 documentattach를 삭제한다. 파일은 documentattach를 삭제 되는 경우 자동 삭제 된다.
    try:
        Document.objects.get(id=int(request.POST['document_id'])).delete()
        return make_response(status=200, content=json.dumps({'success': True}))
    except:
        return make_response(status=400, content=json.dumps({'success': False, 'error': "document delete fail"}))


@login_required
def document_delete(request, document_id):
    document_all = Document.objects.all()
    document_all.filter(id=document_id).delete()
    return redirect('sites_main')


@login_required
def document_attach_delete(request, attachment_id):
    document_attach_all = DocumentAttachment.objects.all()
    document_id = document_attach_all.values(
        "document_id").get(id=attachment_id)
    attach_count = document_attach_all.filter(
        document_id=document_id['document_id']).count()
    if attach_count > 1:
        DocumentAttachment.objects.get(id=attachment_id).delete()
        return redirect('document_attach_detail', document_id['document_id'])
    else:
        Document.objects.get(id=document_id['document_id']).delete()
    return redirect('sites_main')


@login_required
@csrf_exempt
def document_download(request, pk):
    attach_info = DocumentAttachment.objects.get(id=pk)
    filename = os.path.join(settings.MEDIA_ROOT, attach_info.attach.name)
    response = ""
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            response = HttpResponse(FileWrapper(
                f), content_type=attach_info.attach)
            response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'%s' % urllib.parse.quote(
                attach_info.attach_name.encode('utf-8'))
    return response
