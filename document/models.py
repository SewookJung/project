import datetime
import uuid

from django.db import models
from django.dispatch import receiver
from django.contrib.postgres.fields import JSONField
from member.models import Member
from common.models import Client, Product, Mnfacture
from utils.constant import PROJECT_STATUS_CLOSED, PROJECT_STATUS_PROGRESSING


def _documentattachment_upload_path(instance, filename):
    dt = datetime.datetime.now()
    filepath = dt.strftime('%Y/%m/')
    return 'files/{0}/{1}'.format(filepath, uuid.uuid4().hex)


class Document(models.Model):
    CATEGORY_CHOICE = (
        ('PRE', 'Presales'),
        ('PRO', '수행계획서'),
        ('MAN', '유지보수'),
        ('EXA', '검수'),
        ('ETC', '기타'),
    )
    
    client = models.ForeignKey(
        to=Client, null=True, on_delete=models.SET_NULL)
    mnfacture = models.ForeignKey(
        to=Mnfacture, null=True, blank=True, on_delete=models.SET_NULL, )
    product = models.ForeignKey(
        to=Product, null=True, blank=True, on_delete=models.SET_NULL)
    project = models.SmallIntegerField(default=0)
    category = models.CharField(
        max_length=10, choices=CATEGORY_CHOICE, default='PRE')
    creator = models.ForeignKey(
        to=Member, null=True, on_delete=models.SET_NULL)
    auth = JSONField(default=dict, blank=True, null=True, editable=False)
    attach = models.FileField(
        upload_to=_documentattachment_upload_path, default="")
    attach_name = models.CharField(max_length=50, default="")
    content_size = models.CharField(max_length=50, default="")
    content_type = models.CharField(max_length=100, default="")
    check_code = models.CharField(max_length=128, default="")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    update_at = models.DateTimeField(auto_now=True, editable=False)
    comments = models.TextField(blank=True)


class DocumentAttachment(models.Model):
    document = models.ForeignKey(
        to=Document, on_delete=models.CASCADE, null=True)
    attach = models.FileField(
        upload_to=_documentattachment_upload_path, default="")
    attach_name = models.CharField(max_length=50, default="")
    content_size = models.CharField(max_length=50, default="")
    content_type = models.CharField(max_length=100, default="")
    check_code = models.CharField(max_length=128, default="")
    is_state = models.SmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

@receiver(models.signals.post_delete, sender=Document)
def documentattachment_on_post_delete(sender, instance, *args, **kwargs):
    if instance.attach:
        instance.attach.delete(save=False)
