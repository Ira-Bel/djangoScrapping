from django.contrib import admin
from django.contrib.admin.decorators import register
from .models import Goods


@register(Goods)
class ScrappingAdmin(admin.ModelAdmin):
    pass





