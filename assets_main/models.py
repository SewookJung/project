# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from member.models import Member


class Asset(models.Model):

    # 'glowellsystem' - 테스트용, 폐기의 경우 변경된다.
    member_id = models.ForeignKey(
        Member, null=True, blank=True, on_delete=models.SET_NULL)

    mnfacture = models.CharField(max_length=30, default='')  # 제조사명

    model = models.CharField(max_length=40, default='')  # 모델명

    cpu = models.CharField(max_length=30, default='')  # CPU

    memory = models.CharField(max_length=30, default='')  # MEMORY

    harddisk = models.CharField(max_length=30, default='')  # HARDDISK

    is_where = models.CharField(max_length=30, default='')  # 사용처

    # 현재상태 1: 개인사용, 2: TEST, 3: 대여중, 4:폐기
    is_state = models.IntegerField(max_length=1, default='')

    purchase_date = models.DateField(null=True, blank=True)  # 구입일

    created = models.DateTimeField(auto_now_add=True, editable=False)  # 등록날짜

    closed = models.DateField(null=True, blank=True)  # 폐기일

    comments = models.CharField(max_length=200, default='')  # 기타 comment

# Create your models here.
