from django.core.files.base import ContentFile
from django.http import Http404, HttpResponse, QueryDict
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

from .models import Blob, Bucket

# https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectPUT.html


@csrf_exempt
def main(request, bucket_name, path):
    bucket = get_object_or_404(Bucket, name=bucket_name)
    if request.method == 'PUT':
        if not bucket.verify_request(request):
            return HttpResponse(status=403)

        blob = Blob.objects.filter(bucket=bucket, path=path).first()
        if not blob:
            blob = Blob(
                bucket=bucket,
                path=path
            )
        blob.content_type = request.META.get('CONTENT_TYPE', '')
        blob.size = request.META.get('CONTENT_LENGTH', '0')
        blob.file.save(f'{bucket.name}/{path}', ContentFile(request.body))
        blob.save()
        return HttpResponse('')
    elif request.method == 'GET':
        # TODO check that https://djangosnippets.org/snippets/365/
        blob = Blob.objects.filter(bucket=bucket, path=path).first()
        if not blob:
            raise Http404()
        return HttpResponse(blob.file.read(), content_type=blob.content_type)
    elif request.method == 'HEAD':
        if Blob.objects.filter(bucket=bucket, path=path).exists():
            return HttpResponse('')
        else:
            raise Http404()
    else:
        return HttpResponse('')
