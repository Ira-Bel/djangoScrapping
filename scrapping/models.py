from django.db import models


class Goods(models.Model):
    name = models.CharField(max_length=300)
    image_link = models.URLField(max_length=300)
    description = models.TextField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'item'
        verbose_name_plural = 'items'
