import json
import os
import urllib
import uuid
import datetime


from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.conf import settings

from wsgiref.util import FileWrapper

from assets.forms import AssetForm
from .forms import ProjectForm, DocumentAttachmentForm, DocumentForm
from .models import Document, DocumentAttachment, Project
from member.models import Member
from common.views import member_info, member_info_all

from utils.functions import make_response


@login_required
def sites_main(request):
    projects = Project.objects.all()
    documents = Document.objects.all()
    project_id = documents.values('project').distinct()
    documents_array = []
    for item in project_id:
        all_document = documents.filter(
            project=item['project']).order_by('project').distinct()
        for item in all_document:
            rework_document = {"id": item.id, "project": item.project,
                               "member": item.member, "kind": item.kind, "auth": item.auth, "project_id": item.project.id}
            documents_array.append(rework_document)
    return render(request, 'sites/sites_main.html', {"projects": projects, "documents": documents_array})


@login_required
def sites_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    asset_form = AssetForm()
    project_form = ProjectForm()
    document_form = DocumentAttachmentForm()
    return render(request, 'sites/sites_detail.html', {"project": project, "asset_form": asset_form, "project_form": project_form,  "document_form": document_form})


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
    return render(request, "sites/sites_add.html", {'asset_form': asset_form, 'project_form': project_form, 'document_form': document_form, })


@login_required
def sites_add_apply(request):
    if request.method == "POST":
        project_apply = Project(title=request.POST['project_name'], status=request.POST['status'],
                                comments=request.POST['sites_comments'], client_id=request.POST[
            'client'], product_id=request.POST['product'],
            info={"sales": request.POST.getlist('member_name')[0], "mn_cycle": request.POST['cycle'], "eng": request.POST.getlist('member_name')[1], "started_at": request.POST.getlist('purchase_date')[
                0], "ended_at": request.POST.getlist('purchase_date')[1], "mnstarted_at": request.POST.getlist('purchase_date')[2], "mnended_at": request.POST.getlist('purchase_date')[3]}
        )
        project_apply.save()
        return redirect("sites_main")
    else:
        return redirect("sites_main")


@login_required
def document_upload(request):
    document_form = DocumentForm()
    dt = datetime.datetime.now()
    check_code = "{0}-{1}-{2}".format(dt.strftime('%Y%m%d'),
                                      uuid.uuid4().hex, request.session['id'])
    attach_list = DocumentAttachment.objects.all()
    return render(request, "sites/sites_upload.html", {'document_form': document_form, 'attach_list': attach_list, 'check_code': check_code})


@login_required
def document_detail(request, project_id):
    login_id = request.session['id']
    documents = Document.objects.filter(project_id=project_id)
    documents_attach = DocumentAttachment.objects.all()
    documents_id = documents.values("id")
    project_name = documents[0].project
    documents_attach_list = []
    for document_id in documents_id:
        document_file_list = documents_attach.filter(
            document_id=document_id['id'])
        for file in document_file_list:
            document = documents.get(id=file.document_id)
            document_auth_value = [item['value'] for item in document.auth]
            document_auth_value.append(str(document.member_id))
            rework_document_attached = {'id': file.id, 'attach_name': file.attach_name,
                                        'created_at': file.created_at, 'permission': document.auth, 'kind': document.kind, 'member': document.member, 'auth_value': document_auth_value}
            documents_attach_list.append(rework_document_attached)
    return render(request, "sites/document_detail.html", {"documents_attach_list": documents_attach_list, 'project_name': project_name, 'login_id': login_id, })


@login_required
def document_attach_detail(request, attachment_id):
    document_form = DocumentForm()
    document_attach = DocumentAttachment.objects.get(id=attachment_id)
    document = Document.objects.get(id=document_attach.document_id)
    return render(request, "sites/document_attach_detail.html", {'document_attach': document_attach, 'document_form': document_form, 'document': document})


@login_required
def document_attach_detail_apply(request, attachment_id):
    permissions = json.loads(request.POST['permission'])
    document_attach = DocumentAttachment.objects.values(
        'document_id').get(id=attachment_id)
    document = Document.objects.get(id=document_attach['document_id'])
    document.kind = request.POST['kind']
    document.auth = permissions
    document.save()
    return make_response(content=json.dumps({'success': True}))


@login_required
@csrf_exempt
def document_attach_detail_upload_apply(request):
    print(request.POST)
    return make_response(content=json.dumps({'success': True}))


@login_required
def document_attach_auth(request, attachment_id):
    document_attach = DocumentAttachment.objects.get(id=attachment_id)
    document = Document.objects.get(id=document_attach.document_id)
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
    try:
        document_apply = Document(
            project_id=request.POST['project'], member_id=request.session[
                'id'], kind=request.POST['kind'], auth=permission
        )
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
            document_attach_apply = DocumentAttachment(
                attach_name=request.POST['qqfilename'], content_size=request.FILES[
                    'qqfile'].size, content_type=request.FILES['qqfile'].content_type,
                document_id=request.POST['document_id'], attach=request.FILES['qqfile'], check_code=request.POST['check_code']
            )
            document_attach_apply.save()
            return make_response(content=json.dumps({'success': True}))
        except:
            return make_response(status=400, content=json.dumps({'success': False, 'error': "file upload error"}))
    else:
        return make_response(status=400, content=json.dumps({'success': False, 'error': "file upload error"}))


@login_required
@csrf_exempt
def document_reg_delete(request):
    # 파일업로드 과정에서 실패한 경우 신규의 경우 document삭제 및 documentattach를 삭제한다. 파일은 documentattach를 삭제 되는 경우 자동 삭제 된다.
    try:
        Document.objects.get(id=request.POST['document_id']).delete()
        DocumentAttachment.objects.get(
            document=request.POST['document_id'], check_code=request.POST['check_code']).delete()
        return make_response(status=400, content=json.dumps({'success': True}))
    except:
        return make_response(status=400, content=json.dumps({'success': False, 'error': "document delete fail"}))


@login_required
def document_delete(request, attachment_id):
    document_attach = DocumentAttachment.objects.all()
    document_id = document_attach.values(
        'document_id').get(id=attachment_id)
    document_attach_count = document_attach.filter(
        document_id=document_id['document_id']).count()
    if document_attach_count > 1:
        document_attach.get(
            id=attachment_id, document_id=document_id['document_id']).delete()
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
