import datetime
import uuid

from django.db import models
from django.dispatch import receiver

from member.models import Member
from common.models import Client, Product, ProductModel, Mnfacture
from utils.constant import STATUS_KEEP, STATUS_SOLD, STATUS_DISPOSAL, STATUS_RETURN, STATUS_OPERATING, STATUS_RMA


def _equipmentattachment_upload_path(instance, filename):
    dt = datetime.datetime.now()
    filepath = dt.strftime('%Y/%m/')
    return 'files/{0}/{1}'.format(filepath, uuid.uuid4().hex)


class Equipment(models.Model):
    STATUS_CHOICE = (
        (STATUS_OPERATING, STATUS_OPERATING),
        (STATUS_RMA, STATUS_RMA),
        (STATUS_DISPOSAL, STATUS_DISPOSAL),
        (STATUS_RETURN, STATUS_RETURN)
    )

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
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICE, default=STATUS_OPERATING)
    comments = models.CharField(max_length=200, default='')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.serial

    def expire_maintenance_check(self):
        now = datetime.date.today()
        maintenance_date = self.maintenance_date
        remainder_date = now - maintenance_date
        remainder_date_days = remainder_date.days

        data = {}

        if 0 < remainder_date_days:
            data['days'] = abs(remainder_date_days)
            data['expire'] = 'true'

        elif 0 > remainder_date_days:
            data['days'] = abs(remainder_date_days)
            data['expire'] = 'false'

        else:
            datetime_time_max = datetime.time.max
            today_time_max = datetime.datetime.combine(now, datetime_time_max)
            now = datetime.datetime.now()
            remainder_date_hours = str(today_time_max - now).split(':')

            data['hours'] = remainder_date_hours[0]
            data['expire'] = 'false'

        return data


class EquipmentHistory(models.Model):
    STATUS_CHOICE = (
        (STATUS_RMA, STATUS_RMA),
        (STATUS_DISPOSAL, STATUS_DISPOSAL),
        (STATUS_RETURN, STATUS_RETURN)
    )

    equipment = models.ForeignKey(
        Equipment, on_delete=models.SET_NULL, null=True)
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE)
    comments = models.CharField(max_length=200, default='')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


class Stock(models.Model):
    STATUS_CHOICE = (
        (STATUS_KEEP, STATUS_KEEP),
        (STATUS_SOLD, STATUS_SOLD),
        (STATUS_DISPOSAL, STATUS_DISPOSAL),
        (STATUS_RETURN, STATUS_RETURN),
    )

    mnfacture = models.ForeignKey(
        to=Mnfacture, null=True, on_delete=models.SET_NULL)
    product_model = models.ForeignKey(
        to=ProductModel, null=True, on_delete=models.SET_NULL)
    serial = models.CharField(max_length=50, default="")
    location = models.CharField(max_length=100, default="")
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICE, default=STATUS_KEEP)
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
