import json

from django.shortcuts import render, redirect
from django.http import HttpResponse
from assets.forms import AssetForm
from .forms import ProjectForm, DocumentAttachmentForm, DocumentForm
from .models import Document, DocumentAttachment, Project
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View


def make_response(status=200, content_type="text/plain", content=None):
    response = HttpResponse()
    response.status_code = status
    response['Content-Type'] = content_type
    response.content = content
    print(response)
    return response


def sites_main(request):
    projects = Project.objects.all()
    return render(request, 'sites/sites_main.html', {"projects": projects})


def sites_add(request):
    asset_form = AssetForm()
    project_form = ProjectForm()
    document_form = DocumentAttachmentForm()
    return render(request, "sites/sites_add.html", {'asset_form': asset_form, 'project_form': project_form, 'document_form': document_form, })


def sites_add_apply(request):
    if request.method == "POST":
        print(request.POST)
        project_apply = Project(title=request.POST['project_name'], status=request.POST['status'],
                                comments=request.POST['sites_comments'], client_id=request.POST[
                                    'client'], product_id=request.POST['product'],
                                info={"sales": request.POST.getlist('member_name')[0], "mn_cycle": request.POST['cycle'], "eng": request.POST.getlist('member_name')[1], "started_at": request.POST.getlist('purchase_date')[
                                    0], "ended_at": request.POST.getlist('purchase_date')[1], "msstarted_at": request.POST.getlist('purchase_date')[2], "mended_at": request.POST.getlist('purchase_date')[3]}
                                )
        project_apply.save()
        return redirect("sites_main")
    else:
        return redirect("sites_main")


def document_upload(request):
    document_form = DocumentForm()
    return render(request, "sites/sites_upload.html", {'document_form': document_form})


@csrf_exempt
def document_upload_apply(request):
    if request.method == "POST":
        print(request.POST)
        print(request.FILES)

        document_search = Document.objects.filter(
            project_id=request.POST['project'])

        if not document_search:
            try:
                document_apply = Document(
                    project_id=request.POST['project'], member_id=9, kind=request.POST['kind'])
                document_apply.save()
                document_attach_apply = DocumentAttachment(
                    attach_name=request.POST['qqfilename'], upload_name=request.POST['qqfilename'], upload_dir="test", document_id=document_apply.id, attach=request.FILES['qqfile']
                )
                document_attach_apply.save()
                return make_response(content=json.dumps({'success': True}))
            except:
                return make_response(status=400, content=json.dumps({'success': False, 'error': "error message to display"}))

        else:
            try:
                document = Document.objects.filter(
                    project_id=request.POST['project'])

                document_attach_apply = DocumentAttachment(
                    attach_name=request.POST['qqfilename'], upload_name=request.POST['qqfilename'], upload_dir="test", document_id=document[0].id, attach=request.FILES['qqfile']
                )
                document_attach_apply.save()
                return make_response(content=json.dumps({'success': True}))
            except:
                return make_response(status=400, content=json.dumps({'success': False, 'error': "error message to display"}))
    else:
        return redirect("sites_main")
