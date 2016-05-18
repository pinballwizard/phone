from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from phonebook import views as phonebook_views
from sms import views as sms_views

from django.views.generic import TemplateView

sms_urls = [
    url(r'^post_sms', sms_views.test_sms, name='test_sms'),
    url(r'^stats', sms_views.smsstats, name='stats'),
]

phonebook_urls = [
    url(r'^$', phonebook_views.phonebook_page, name='phonebook'),
    url(r'^refresh', phonebook_views.refresh, name='refresh'),
    url(r'^stats', phonebook_views.call_stats, name='stats'),
]

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url('^', include('django.contrib.auth.urls')),
    url('^', include(phonebook_urls, namespace='phonebook', app_name='phonebook')),
    url(r'^sms/', include(sms_urls, namespace='sms', app_name='sms')),
    url(r'^receive', sms_views.get_sms, name='get_sms'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)