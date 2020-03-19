from django.shortcuts import render, redirect


def document_main(request):
    return render(request, 'document/document_main.html', {})
