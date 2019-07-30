from django.contrib import admin

from .models import Blob, Bucket


class BlobAdmin(admin.ModelAdmin):
    list_display = ['bucket', 'path', 'content_type', 'size']
    readonly_fields = ['bucket', 'path', 'content_type', 'size']
    exclude = ['file']


class BucketAdmin(admin.ModelAdmin):
    list_display = ['name', 'access_key_id', 'size']

admin.site.register(Blob, BlobAdmin)
admin.site.register(Bucket, BucketAdmin)
