from django.shortcuts import render, redirect
from assets.forms import AssetForm
from .forms import ProjectForm
from .models import Project
# Create your views here.


def sites_main(request):
    return render(request, 'sites/sites_main.html', {})


def sites_add(request):
    asset_form = AssetForm()
    project_form = ProjectForm()
    return render(request, "sites/sites_add.html", {'asset_form': asset_form, 'project_form': project_form})


def sites_add_apply(request):
    if request.method == "POST":
        project_apply = Project(title=request.POST['project_name'], status=request.POST['status'], comments=request.POST['comments'],
                                client_id=request.POST['client_id'], product_id=request.POST[
                                    'product_id'],  model_id=request.POST['model_id'],
                                info={"sales": request.POST['sales'], "started_at": request.POST['pjStDate'], "ended_at": request.POST['pjEdDate'], "msstarted_at": request.POST['mnStDate'], "mended_at": request.POST['mnEdDate'], "eng": request.POST['eng']})
        project_apply.save()
        return redirect('sites_main')
    else:
        return render(request, "sites/sites_add.html", {})
