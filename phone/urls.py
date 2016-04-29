from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from phonebook import views as phonebook_views

from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url('^', include('django.contrib.auth.urls')),
    url(r'^$', phonebook_views.phonebook_page, name='phonebook'),
    url(r'^refresh', phonebook_views.config_parse, name='refresh'),
    url(r'^panel', phonebook_views.ext_panel_parse, name='panel'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)