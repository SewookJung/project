from django.shortcuts import render

# Create your views here.


def document_main(request):
    return render(request, 'document/document_main.html', {})


def document_search(request):
    return render(request, "document/document_search.html", {})


def document_add(request):
    return render(request, "document/document_add.html", {})
