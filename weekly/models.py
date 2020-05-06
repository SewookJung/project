from django.db import models

from datetime import datetime

from common.models import Client, Product
from member.models import Member
from utils.constant import WEEKLY_STATUS_PRE, WEEKLY_STATUS_POST, WEEKLY_STATUS_ETC, WEEKLY_STATUS_MAINTANCE

# Create your models here.


class Report(models.Model):

    SALES_TYPE_CHOICE = (
        (WEEKLY_STATUS_PRE, 'PRESALES'),
        (WEEKLY_STATUS_POST, 'POSTSALES'),
        (WEEKLY_STATUS_MAINTANCE, 'MAINTANCE'),
        (WEEKLY_STATUS_ETC, 'ETC')
    )

    client = models.ForeignKey(
        to=Client, null=True, blank=True, on_delete=models.CASCADE)
    member = models.ForeignKey(
        to=Member, null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(
        to=Product, null=True, blank=True, on_delete=models.CASCADE)
    client_manager = models.CharField(max_length=50, default="")
    sales_type = models.CharField(max_length=10, choices=SALES_TYPE_CHOICE,
                                  default=WEEKLY_STATUS_PRE, help_text='선택해주세요')
    support_comment = models.CharField(max_length=1024, default="")
    support_date = models.DateField(default=datetime.now)
    comments = models.CharField(max_length=1024, default="")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    update_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['client']

    @property
    def client_name(self):
        client_name = Client.objects.get(
            id=self.client_id)
        return client_name

    @property
    def product_name(self):
        product_name = Product.objects.get(
            id=self.product_id)
        return product_name
