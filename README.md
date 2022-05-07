# Your Own Amazon S3 Server

This application replicate basic Amazon S3 functionality:
 - Ability to have multiple Buckets with own credentials
 - Upload files with public read-only access

Main purpose of that application is to store Media and Static files of Django applications outside of the application instance.
That is especially useful if your deploy application to the cloud providers (for ex. Heroku) which does not offer storage option.

## Deployment

Create `docker.env` file with:

 - `SECRET_KEY` - Django Secret Key

 Build and Run via:
 ```
 docker-compose up -d
 ```

Create an Administrator account:

```
docker-compose exec app python ./manage.py createsuperuser
```

## Using in your Application

In order to use that storage at your Django projects you may need use `django-storages` package, in that case some extra settings required.
```python
# Usual AWS S3 Configuration
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']

# Some extra setings
AWS_S3_ENDPOINT_URL='https://your.app.instance.com'  # Your App Endpoint
AWS_QUERYSTRING_AUTH = False
AWS_DEFAULT_ACL='public-read'
 ```

### Demo project

Demo project, which utilize that app available [here](https://github.com/slyapustin/django-classified-demo).
