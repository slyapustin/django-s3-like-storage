from django.contrib import admin

from .models import Blob, Bucket


class BlobAdmin(admin.ModelAdmin):
    list_display = ['bucket', 'path', 'content_type', 'size']
    readonly_fields = ['bucket', 'path', 'file', 'content_type', 'size']


class BucketAdmin(admin.ModelAdmin):
    list_display = ['name', ]

admin.site.register(Blob, BlobAdmin)
admin.site.register(Bucket, BucketAdmin)
