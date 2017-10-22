from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static

from core import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.IndexView.as_view(), name='index')
] + static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT,
) + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
