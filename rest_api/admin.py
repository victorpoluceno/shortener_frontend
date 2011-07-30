from django.contrib import admin

from tastypie.models import ApiKey


class ApiKeyAdmin(admin.ModelAdmin):
    pass

admin.site.register(ApiKey, ApiKeyAdmin)
