import datetime
import uuid

from django.db import models
from django.dispatch import receiver
from django.contrib.postgres.fields import JSONField
from member.models import Member
from utils.constant import PROJECT_STATUS_CLOSED, PROJECT_STATUS_PROGRESSING


class Project(models.Model):
    PROJECT_STATUS_CHOICE = (
        (PROJECT_STATUS_CLOSED, 'CLOSED'),
        (PROJECT_STATUS_PROGRESSING, 'PROGRESSING')
    )
    title = models.CharField(max_length=100)
    member = models.ForeignKey(
        to=Member, null=True, blank=True, on_delete=models.SET_NULL)
    client = models.ForeignKey(
        to='common.Client', null=True, blank=True, verbose_name='the related client', on_delete=models.SET_NULL)
    product = models.ForeignKey(
        to='common.Product', null=True, blank=True, verbose_name='the related product', on_delete=models.SET_NULL)
    info = JSONField(default=dict, blank=True,
                     null=True, editable=False)
    status = models.CharField(
        max_length=1, choices=PROJECT_STATUS_CHOICE, default=PROJECT_STATUS_CLOSED, help_text='선택해주세요')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    update_at = models.DateTimeField(auto_now=True, editable=False)
    comments = models.TextField()

    class Meta:
        unique_together = (('title', 'product'),)

    PRE = "PRE"
    PRO = "PRO"
    EXA = "EXA"
    ETC = "ETC"
    MAN = "MAN"

    WORK_STEP_CHOICE = (
        (PRE, "Presales"),
        (PRO, "Project Progressing"),
        (EXA, "Examination"),
        (MAN, "Maintenance"),
        (ETC, "ETC")
    )

    def __str__(self):
        return self.title


class Document(models.Model):
    A = "A"
    B = "B"
    C = "C"
    D = "D"

    PRE_MIDDLE_CLASS_CHOICE = (
        ("WBS", "WBS"),
        ("제안서", "제안서"),
        ("제품소개서", "제품소개서"),
        ("계약서", "계약서")
    )

    PRO_MIDDLE_CLASS_CHOICE = (
        ("견적서", "견적서"),
        ("발주서", "발주서"),
        ("고객사 요구사항", "고객사 요구사항")
    )

    EXA_MIDDLE_CLASS_CHOICE = (
        ("검수확인서", "검수확인서"),
        ("세금계산서", "세금계산서"),
    )

    ETC_MIDDLE_CLASS_CHOICE = (
        ("기타", "기타"),
    )

    MAN_MIDDLE_CLASS_CHOICE = (
        ("유지보수 계약서", "유지보수 계약서"),
    )

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, null=True)
    member = models.ForeignKey(
        to=Member, null=True, blank=True, on_delete=models.SET_NULL)
    auth = JSONField(default=dict, blank=True,
                     null=True, editable=False)
    kind = models.CharField(
        max_length=3, choices=Project.WORK_STEP_CHOICE, default=Project.ETC)
    pre_middle_class = models.CharField(
        max_length=10, choices=PRE_MIDDLE_CLASS_CHOICE, null=True, blank=True)
    pro_middle_class = models.CharField(
        max_length=10, choices=PRO_MIDDLE_CLASS_CHOICE, null=True, blank=True)
    exa_middle_class = models.CharField(
        max_length=10, choices=EXA_MIDDLE_CLASS_CHOICE, null=True, blank=True)
    man_middle_class = models.CharField(
        max_length=10, choices=MAN_MIDDLE_CLASS_CHOICE, null=True, blank=True)
    etc_middle_class = models.CharField(
        max_length=10, choices=ETC_MIDDLE_CLASS_CHOICE, null=True, blank=True)
    comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.project.title


def _documentattachment_upload_path(instance, filename):
    dt = datetime.datetime.now()
    filepath = dt.strftime('%Y/%m/')
    return 'files/{0}/{1}'.format(filepath, uuid.uuid4().hex)


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


@receiver(models.signals.pre_save, sender=DocumentAttachment)
def documentattachment_on_pre_save(sender, instance, *args, **kwargs):
    if instance.pk:
        try:
            obj = sender.objects.get(pk=instance.pk)
            if obj.attach != instance.attach_name:
                obj.attach.delete(save=False)
        except sender.DoesNotExist:
            pass


@receiver(models.signals.post_delete, sender=DocumentAttachment)
def documentattachment_on_post_delete(sender, instance, *args, **kwargs):
    if instance.attach:
        instance.attach.delete(save=False)
