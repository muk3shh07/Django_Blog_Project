from django.contrib import admin
from .models import Category, Blog, Product

# Register your models here.
admin.site.register((Category, Blog, Product))
