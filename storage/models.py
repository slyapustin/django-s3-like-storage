import logging
import random
import string

import awssig
from django.core.validators import MinLengthValidator, validate_slug
from django.db import models
from django.db.models import Sum
from django.template.defaultfilters import filesizeformat
from django.urls import reverse

logger = logging.getLogger(__name__)


class Bucket(models.Model):
    # https://docs.aws.amazon.com/AmazonS3/latest/dev/BucketRestrictions.html
    name = models.CharField(validators=[MinLengthValidator(3), validate_slug], max_length=63, unique=True)
    access_key = models.CharField(max_length=16, default='', blank=True)
    secret_key = models.CharField(max_length=128, default='', blank=True)

    def __str__(self):
        return self.name

    def verify_request(self, request):
        headers={
            "X-Amz-Date": request.META.get('HTTP_X_AMZ_DATE', ''),
            "x-amz-date": request.META.get('HTTP_X_AMZ_DATE', ''),
            "authorization": request.META.get('HTTP_AUTHORIZATION', ''),
            'content-md5': request.META.get('HTTP_CONTENT_MD5', ''),
            'content-type': request.META.get('CONTENT_TYPE', ''),
            'host': request.META.get('HTTP_HOST', ''),
            'x-amz-acl': request.META.get('HTTP_X_AMZ_ACL', ''),
            'x-amz-content-sha256': request.META.get('HTTP_X_AMZ_CONTENT_SHA256', '')
        }
        v = awssig.AWSSigV4Verifier(
            request_method=request.method,
            uri_path=request.META.get('PATH_INFO', ''),
            query_string=request.META.get('QUERY_STRING', ''),
            headers=headers,
            body=request.body,
            region="us-east-1",
            service="s3",
            key_mapping={self.access_key: self.secret_key},
            timestamp_mismatch=None)
        try:
            v.verify()
            return True
        except awssig.InvalidSignatureError as e:
            logger.warning('Invalid signature: %s', e)
        except Exception as e:
            logger.error('Unable to verify request: %s', e)

        return False

    @property
    def size(self):
        return filesizeformat(self.blob_set.aggregate(Sum('size')).get('size__sum', 0))

    def save(self, *args, **kwargs):
        if not self.access_key:
            self.access_key = ''.join(random.choice(
                string.ascii_letters + string.digits) for i in range(16))
        if not self.secret_key:
            self.secret_key = ''.join(random.choice(
                string.ascii_letters + string.digits) for i in range(32))

        super().save(*args, **kwargs)


class Blob(models.Model):
    bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE)
    path = models.CharField(max_length=512)
    file = models.FileField()

    # TODO move extra meta fields to the PostgreSQL JSONField
    content_type = models.CharField(max_length=512, default='')
    size = models.IntegerField(default=0)

    def __str__(self):
        return self.path
    
    def get_absolute_url(self):
        return reverse(
            'public_link', 
            kwargs={
                'bucket_name': self.bucket.name, 
                'path': self.path
                }
            )
