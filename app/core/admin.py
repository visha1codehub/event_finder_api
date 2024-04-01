"""
Admin for core..
"""

from django.contrib import admin

from .models import Event


admin.site.register(Event)
# from import_export.admin import ImportExportModelAdmin

# @admin.register(Event)
# class CustomerData(ImportExportModelAdmin):
#     pass
