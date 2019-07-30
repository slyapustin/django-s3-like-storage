# Your own Amazon S3 Django server

This application replicate basic Amazon S3 functionality:
 - Ability to have multiple Buckets with own credentials
 - Upload files with public read-only access

Main purpose of that application is to store Media and Static files of Django applications outside of the application instance.
That is especially useful if your deploy application to the cloud providers (for ex. Heroku) which does not offer storage option.

## Deployment

Create Administrator account:
`docker-compose exec app python ./manage.py createsuperuser`
