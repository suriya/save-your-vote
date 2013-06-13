from django.conf.urls import patterns, include, url
from voterreg.views import facebook_login, home_page

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', home_page, name='home'),
    url(r'^voterreg/', include('voterreg.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^facebook/', include('django_facebook.urls')),
    url(r'^accounts/', include('django_facebook.auth_urls')),
    url(r'^facebook-login/', facebook_login, name='facebook-login'),
    # url(r'^accounts/', include('userena..urls')),
    # url(r'^accounts/', include('registration.backends.default.urls')),
)