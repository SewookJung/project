import json
import os
import urllib
import uuid
import datetime

from django.shortcuts import render, resolve_url, reverse
from django.http import HttpResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings

from wsgiref.util import FileWrapper

from assets.forms import AssetForm
from equipment.forms import EquipmentForm
from .forms import DocumentForm, DocumentBasicForms
from .models import Document, DocumentBasicForm
from project.models import Project
from member.models import Member
from common.models import Product, Client
from common.views import member_info, member_info_all

from utils.functions import make_response
from utils.constant import REPORT_PERMISSION_DEFAULT
        
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

@login_required
def document_form(request):
    document_basic_form_objects = DocumentBasicForm.objects.all()
    document_basic_form = DocumentBasicForms()
    dt = datetime.datetime.now()
    check_code = "{0}-{1}-{2}".format(dt.strftime('%Y%m%d'),
                                      uuid.uuid4().hex, request.session['id'])
    login_id = request.session['id']
    
    return render(request, 'document/document_form.html', {'document_basic_form': document_basic_form,'document_basic_form_objects': document_basic_form_objects, 'check_code': check_code, 'login_id':login_id, 'permission': REPORT_PERMISSION_DEFAULT})


#Call Api functions
@login_required
def document(request, document_id):
    if request.method == "DELETE":
        try:
            document = Document.objects.get(id=document_id)
            creator = document.creator_id
            login_id = request.session['id']

            if creator == login_id:
                document.delete()
                return make_response(status=200, content=json.dumps({'success': True, 'msg': '문서가 삭제 되었습니다.'}))
            
            else:
                return make_response(status=400, content=json.dumps({'success': False, 'msg': '해당 문서를 삭제할 수 있는 권한이 없습니다.'}))

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
def document_permission_check(request, document_id):
    attach_info = Document.objects.get(id=document_id)
    creator = attach_info.creator_id
    permissioners = attach_info.auth
    login_id = request.session['id']

    if request.method == "GET":
        if login_id == creator:
            return make_response(status=200, content=json.dumps({'success': True}))
    
        else:
            permissioners_array = []
            for permissioner in permissioners:
                permissioners_array.append(int(permissioner['value']))
            
            if login_id in permissioners_array:
                return make_response(status=200, content=json.dumps({'success': True}))
            else:
                return make_response(status=400, content=json.dumps({'success': False, 'msg': "해당 문서에 대한 다운로드 권한이 없습니다."}))


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
def document_basic_form(request, document_id):
    if request.method == "GET":
        attach_info = DocumentBasicForm.objects.get(id=document_id)
        filename = os.path.join(settings.MEDIA_ROOT, attach_info.attach.name)

        if not os.path.exists(settings.MEDIA_ROOT):
            return make_response(status=400, content=json.dumps({'success': False, 'msg': "NAS서버와 연결이 해제되어 파일 업로드가 불가능합니다.\n관리자에게 문의 바랍니다."}))

        elif not os.path.exists(filename): 
            return make_response(status=400, content=json.dumps({'success': False, 'msg': "해당 문서가 서버에 존재하지 않아 다운로드 할 수 없습니다.\n관리자에게 문의 바랍니다."}))
        
        else:
            return make_response(status=200, content=json.dumps({'success': True}))



@login_required
@csrf_exempt
def document_form_upload_apply(request):
    title = request.POST['title']
    attach_name = request.POST['qqfilename']
    check_code = request.POST['checkCode']
    description = request.POST['desc']
    attach=request.FILES['qqfile']
    content_size=request.FILES['qqfile'].size
    content_type=request.FILES['qqfile'].content_type
    
    try:
        document_basic_form = DocumentBasicForm(title=title, attach_name=attach_name, attach=attach, check_code=check_code, description=description, content_size=content_size, content_type=content_type, creator_id=request.session['id'])
        document_basic_form.save()
        return make_response(status=200, content=json.dumps({'success': True, 'msg': "양식 등록에 성공 하였습니다."}))

    except:
        return make_response(status=400, content=json.dumps({'success': False, 'msg': "양식 등록에 실패하였습니다.\n다시 시도해주시기 바랍니다."}))


@login_required
@csrf_exempt
def document_basic_form_download(request, document_id):
    attach_info = DocumentBasicForm.objects.get(id=document_id)
    filename = os.path.join(settings.MEDIA_ROOT, attach_info.attach.name)
    response = ""

    with open(filename, 'rb') as f:
            response = HttpResponse(FileWrapper(
                f), content_type=attach_info.attach)
            response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'%s' % urllib.parse.quote(
                attach_info.attach_name.encode('utf-8'))
    return response


@login_required
def document_basic_form_delete(request, document_id):
    if request.method == "DELETE":
        try:
            document_basic_form = DocumentBasicForm.objects.get(id=document_id)
            document_basic_form.delete()
            return make_response(status=200, content=json.dumps({'success': True, 'msg': "양식을 삭제하는데 성공하였습니다."}))

        except DocumentBasicForm.DoesNotExist:
            return make_response(status=400, content=json.dumps({'success': False, 'msg': '문서가 서버에 존재하지 않습니다.\n관리자에게 문의하세요.'}))

        except:
            return make_response(status=400, content=json.dumps({'success': False, 'msg': '문서를 삭제하는데 실패하였습니다.\n다시 시도해주세요.'}))
