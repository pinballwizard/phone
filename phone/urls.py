from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from phonebook import views as phonebook_views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', phonebook_views.phonebook_page, name='phonebook'),
    url(r'^reload', phonebook_views.config_reload, name='reload'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)