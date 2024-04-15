from django.contrib import admin

from rest_framework.authtoken.admin import TokenAdmin

from .models import Task

admin.site.register(Task)

TokenAdmin.raw_id_fields = ['user']