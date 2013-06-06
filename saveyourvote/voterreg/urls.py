
from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^epic/new/$', views.epic_new, name='epic-new'),
    url(r'^epic/list/$', views.epic_list, name='epic-list'),
    url(r'^epic/(\d+)/$', views.epic_info, name='epic-info'),
    url(r'^epic/(\d+)/delete/$', views.epic_delete, name='epic-delete'),
#     url(r'^epic/(\d+)/refresh/$', views.epic_refresh, name='epic-refresh'),
)
