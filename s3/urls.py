from django.urls import path

from . import views

urlpatterns = [
    path('<slug:bucket_name>/<path:path>', views.main),
]
