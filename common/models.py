from django.db import models
from django.contrib.postgres.fields import JSONField


class Dept(models.Model):
    name = models.CharField(max_length=20, default='')
    updept_id = models.IntegerField(default=0)
    depth = models.SmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


class Client(models.Model):
    name = models.CharField(max_length=20, default='')
    similiar_word = JSONField(default=dict, blank=True,
                              null=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


class Product(models.Model):
    name = models.CharField(max_length=20, default='')
    makers = models.CharField(max_length=20, default='')
    name = models.CharField(max_length=20, default='')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


class ProductModel(models.Model):
    name = models.CharField(max_length=20, default='')
    product_id = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
