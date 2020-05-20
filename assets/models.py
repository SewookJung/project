# -*- coding: utf-8 -*-

from django.db import models
from member.models import Member

from utils.constant import STATUS_RENTAL


class Asset(models.Model):

    # 'glowellsystem' - 테스트용, 폐기의 경우 변경된다.
    member_name = models.ForeignKey(
        Member, null=True, on_delete=models.SET_NULL)
    mnfacture = models.CharField(max_length=128, default='')  # 제조사명
    model = models.CharField(max_length=128, default='')  # 모델명
    serial = models.CharField(max_length=128, default='')  # Serial
    cpu = models.CharField(max_length=128, default='')  # CPU
    memory = models.CharField(max_length=128, default='')  # MEMORY
    harddisk = models.CharField(max_length=128, default='')  # HARDDISK
    is_where = models.CharField(max_length=128, default='')  # 사용처
    # 현재상태 1: 개인사용, 2: TEST, 3: 대여중, 4:폐기 5: 보관
    is_state = models.IntegerField(default=1)
    purchase_date = models.DateField(null=True, blank=True)  # 구입일
    created = models.DateTimeField(auto_now_add=True, editable=False)  # 등록날짜
    closed = models.DateField(null=True, blank=True)  # 폐기일
    comments = models.CharField(
        max_length=1024, default='', blank=True)  # 기타 comment

    def __str__(self):
        return self.model

    @property
    def renter(self):
        renter = ''
        if self.is_state == STATUS_RENTAL:
            rent = Assetrent.objects.filter(asset_id=self.id).order_by(
                '-id').values_list('member_name')
            renter = rent[0][0]
        return renter

    @property
    def rent_id(self):
        rent_id = ''
        if self.is_state == STATUS_RENTAL:
            rent = Assetrent.objects.filter(
                asset_id=self.id).order_by('-id').values_list('id')
            rent_id = rent[0][0]
        return rent_id

    @property
    def rent_comment(self):
        rent_comment = ''
        if self.is_state == STATUS_RENTAL:
            rent = Assetrent.objects.filter(asset_id=self.id).order_by(
                '-id').values_list('comments')
            rent_comment = rent[0][0]
        return rent_comment


class Assetrent(models.Model):
    asset = models.ForeignKey(to=Asset, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)  # 생성일
    stdate = models.DateField(null=True)  # 대여일
    eddate = models.DateField(null=True)  # 반납예정일
    member_name = models.CharField(max_length=20, default='')  # 빌린 member name
    return_date = models.DateField(null=True, blank=True)  # 반납일
    comments = models.CharField(max_length=200, default='')  # 기타
