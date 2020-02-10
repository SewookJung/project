from django.shortcuts import render

# Create your views here.


def project_main(request):
    return render(request, 'project/project_main.html', {})
