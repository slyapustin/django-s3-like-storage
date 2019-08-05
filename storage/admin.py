from django.contrib import admin

from .models import Blob, Bucket


class BlobAdmin(admin.ModelAdmin):
    list_display = ['bucket', 'path', 'content_type', 'size', 'created_on']
    readonly_fields = ['bucket', 'path', 'content_type', 'size']
    exclude = ['file']
    list_filter = ['created_on', 'updated_on']
    search_fields = ['path']


class BucketAdmin(admin.ModelAdmin):
    list_display = ['name', 'access_key_id', 'size']
    search_fields = ['name']

admin.site.register(Blob, BlobAdmin)
admin.site.register(Bucket, BucketAdmin)
