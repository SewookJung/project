# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


def assets_main(request):
    return render(request, 'assets_main/assets_main.html', {})


def assets_add(request):
    return render(request, 'assets_main/assets_add.html', {})


def assets_status(request):
    return render(request, 'assets_main/assets_status.html', {})
