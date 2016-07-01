from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = [

    url(r'^fishingcontest/', include('fishingcontest.urls')),
	url(r'^admin/', include(admin.site.urls))
]
