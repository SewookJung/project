from django.db import models

from common.models import Client, Product, Mnfacture
from member.models import Member

from utils.constant import PROJECT_STATUS_CLOSED, PROJECT_STATUS_PROGRESSING

class Project(models.Model):
    PROJECT_STATUS_CHOICE = (
        (PROJECT_STATUS_PROGRESSING, "진행 중"),
        (PROJECT_STATUS_CLOSED, "진행 완료"),
    )
    title = models.CharField(max_length=100)
    client = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL)
    mnfacture = models.ForeignKey(Mnfacture, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    creator = models.ForeignKey(Member, null=True, on_delete=models.SET_NULL)
    status = models.CharField(
        max_length=10, choices=PROJECT_STATUS_CHOICE, default=PROJECT_STATUS_PROGRESSING)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    comments = models.TextField(blank=True)

    def __str__(self):
        return self.title