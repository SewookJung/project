import datetime
import uuid

from django.db import models
from django.dispatch import receiver
from member.models import Member
from common.models import Client, Product, ProductModel, Mnfacture
from utils.constant import STOCK_STATUS_KEEP, STOCK_STATUS_SOLD, STOCK_STATUS_DISPOSAL, STOCK_STATUS_RETURN


def _equipmentattachment_upload_path(instance, filename):
    dt = datetime.datetime.now()
    filepath = dt.strftime('%Y/%m/')
    return 'files/{0}/{1}'.format(filepath, uuid.uuid4().hex)


class Equipment(models.Model):
    client = models.ForeignKey(
        to=Client, null=True, on_delete=models.SET_NULL)
    creator = models.ForeignKey(
        to=Member, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(
        to=Product, null=True, on_delete=models.SET_NULL)
    product_model = models.ForeignKey(
        to=ProductModel, null=True, on_delete=models.SET_NULL)
    mnfacture = models.ForeignKey(
        to=Mnfacture, null=True, on_delete=models.SET_NULL)

    serial = models.CharField(max_length=50, default="")
    location = models.CharField(max_length=100, default="")
    install_date = models.DateField(max_length=20, blank=True)
    maintenance_date = models.DateField(max_length=20, blank=True, null=True)
    manager = models.CharField(max_length=50, default="")
    comments = models.CharField(max_length=200, default='')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


class Stock(models.Model):
    STOCK_STATUS_CHOICE = (
        (STOCK_STATUS_KEEP, STOCK_STATUS_KEEP),
        (STOCK_STATUS_SOLD, STOCK_STATUS_SOLD),
        (STOCK_STATUS_DISPOSAL, STOCK_STATUS_DISPOSAL),
        (STOCK_STATUS_RETURN, STOCK_STATUS_RETURN)
    )

    mnfacture = models.ForeignKey(
        to=Mnfacture, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(
        to=Product, null=True, on_delete=models.SET_NULL)
    product_model = models.ForeignKey(
        to=ProductModel, null=True, on_delete=models.SET_NULL)
    serial = models.CharField(max_length=50, default="")
    location = models.CharField(max_length=100, default="")
    status = models.CharField(
        max_length=10, choices=STOCK_STATUS_CHOICE, default="keep")
    receive_date = models.DateField(max_length=20, blank=True)
    return_date = models.DateField(max_length=20, blank=True, null=True)
    disposal_date = models.DateField(max_length=20, blank=True, null=True)
    creator = models.ForeignKey(
        to=Member, on_delete=models.SET_NULL, null=True)
    comments = models.CharField(max_length=200, default='')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


class EquipmentAttachment(models.Model):
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    attach = models.FileField(
        upload_to=_equipmentattachment_upload_path, default="")
    attach_name = models.CharField(max_length=50, default="")
    content_size = models.CharField(max_length=50, default="")
    content_type = models.CharField(max_length=100, default="")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


class StockAttachment(models.Model):
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    attach = models.FileField(
        upload_to=_equipmentattachment_upload_path, default="")
    attach_name = models.CharField(max_length=50, default="")
    content_size = models.CharField(max_length=50, default="")
    content_type = models.CharField(max_length=100, default="")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


@receiver(models.signals.pre_save, sender=StockAttachment)
def stockattachment_on_pre_save(sender, instance, *args, **kwargs):
    if instance.pk:
        try:
            obj = sender.objects.get(pk=instance.pk)
            if obj.attach != instance.attach_name:
                obj.attach.delete(save=False)
        except sender.DoesNotExist:
            pass


@receiver(models.signals.post_delete, sender=StockAttachment)
def stockattachment_on_post_delete(sender, instance, *args, **kwargs):
    if instance.attach:
        instance.attach.delete(save=False)


@receiver(models.signals.pre_save, sender=EquipmentAttachment)
def equipmentattachment_on_pre_save(sender, instance, *args, **kwargs):
    if instance.pk:
        try:
            obj = sender.objects.get(pk=instance.pk)
            if obj.attach != instance.attach_name:
                obj.attach.delete(save=False)
        except sender.DoesNotExist:
            pass


@receiver(models.signals.post_delete, sender=EquipmentAttachment)
def equipmentattachment_on_post_delete(sender, instance, *args, **kwargs):
    if instance.attach:
        instance.attach.delete(save=False)
