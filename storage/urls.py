from django.urls import path

from storage import views

urlpatterns = [
    path('<slug:bucket_name>/<path:path>', views.main, name='public_link'),
]
