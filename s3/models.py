from django.core.validators import MinLengthValidator
from django.db import models


class Bucket(models.Model):
    # https://docs.aws.amazon.com/AmazonS3/latest/dev/BucketRestrictions.html
    name = models.CharField(validators=[MinLengthValidator(3)], max_length=63)

    def __str__(self):
        return self.name

    def has_write_permission(self, request):
        # TODO check HTTP_AUTHORIZATION header
        return True 


class Blob(models.Model):
    bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE)
    path = models.CharField(max_length=512)
    file = models.FileField()

    # TODO move extra meta fields to the PostgreSQL JSONField
    content_type = models.CharField(max_length=512, default='')
    size = models.IntegerField(default=0)

    def __str__(self):
        return self.path
