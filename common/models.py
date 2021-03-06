from django.db import models
from django.contrib.postgres.fields import JSONField


class Dept(models.Model):
    name = models.CharField(max_length=20, default='', )
    updept_id = models.IntegerField(default=0)
    depth = models.SmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


class Client(models.Model):
    name = models.CharField(max_length=40, default='',)
    similar_word = JSONField(default=dict, blank=True,
                             null=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    def natural_key(self):
        return (self.name)


class Mnfacture(models.Model):
    manafacture = models.CharField(max_length=40, default='',)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def natural_key(self):
        return (self.manafacture)

    def __str__(self):
        return self.manafacture

    class Meta:
        ordering = ['manafacture']


class Product(models.Model):
    name = models.CharField(max_length=40, default='',)
    makers = models.CharField(max_length=40, default='')
    mnfacture = models.ForeignKey(
        Mnfacture, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    level = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class ProductModel(models.Model):
    name = models.CharField(max_length=40, default='',)
    product_id = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        unique_together = (('name'),)

    def natural_key(self):
        return (self.name)
