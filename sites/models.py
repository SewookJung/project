from django.db import models
from django.dispatch import receiver
from django.contrib.postgres.fields import JSONField
from member.models import Member


class Project(models.Model):
    PROJECT_STATUS_CHOICE = (
        ('C', 'CLOSED'),
        ('P', 'PROGRESSING')
    )
    title = models.CharField(max_length=30)
    client_id = models.ForeignKey(
        to='common.Client', null=True, blank=True, verbose_name='the related client', on_delete=models.SET_NULL)
    product_id = models.ForeignKey(
        to='common.Product', null=True, blank=True, verbose_name='the related product', on_delete=models.SET_NULL)
    sales = models.ForeignKey(to=Member, null=True,
                              blank=True, on_delete=models.SET_NULL)
    status = models.CharField(
        max_length=1, choices=PROJECT_STATUS_CHOICE, default='C', help_text='선택해주세요')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    update_at = models.DateTimeField(auto_now=True, editable=False)
    comments = models.TextField()

    class Meta:
        unique_together = (('title', 'product_id'),)

    PRE = "PRE"
    PRO = "PRO"
    EXA = "EXA"
    REV = "REV"
    ETC = "ETC"
    MAN = "MAN"

    WORK_STEP_CHOICE = (
        (PRE, "Presales"),
        (PRO, "Project Progressing"),
        (EXA, "Examination"),
        (MAN, "Maintenace"),
        (ETC, "ETC")
    )

    WORK_STEP_CHOICE = (
        (PRE,
            ("PRD", "제품소개서"),
         ),
        (PRO, "Project Progressing"),
        (EXA, "Examination"),
        (MAN, "Maintenace"),
        (ETC, "ETC")
    )


class Document(models.Model):
    title = models.CharField(max_length=40)
    project_id = models.ForeignKey(
        Project, on_delete=models.SET_NULL, null=True)
    member_id = models.ForeignKey(
        to=Member, null=True, blank=True, on_delete=models.SET_NULL)
    kind = models.CharField(
        max_length=1, choices=Project.PROJECT_STATUS_CHOICE, default=Project.ETC)
    comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


class DocumentAuth(models.Model):
    document = models.ForeignKey(
        Document, on_delete=models.SET_NULL, null=True)
    members = JSONField(default=dict, blank=True,
                        null=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


def _documentattatchment_upload_path(instance, filename):
    return 'document/{0}/document/{1}/{2}'.format(
        instance.document.project_id, instance.document.pk, filename)


class DocumentAttachment(models.Model):
    document = models.ForeignKey(
        Document, on_delete=models.SET_NULL, null=True)
    attach = models.FileField(
        upload_to=_documentattatchment_upload_path)


@receiver(models.signals.pre_save, sender=DocumentAttachment)
def documentattachment_on_pre_save(sender, instance, *args, **kwargs):
    if instance.pk:
        try:
            obj = sender.objects.get(pk=instance.pk)
            if obj.attach != instance.attach:
                obj.attach.delete(save=False)
        except sender.DoesNotExist:
            pass


@receiver(models.signals.post_delete, sender=DocumentAttachment)
def documentattachment_on_post_delete(sender, instance, *args, **kwargs):
    if instance.attach:
        instance.attach.delete(save=False)
