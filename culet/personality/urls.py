from django.conf.urls.defaults import *


urlpatterns = patterns('culet.personality.views',
    url(r'become/(?P<alternate>[\w-]+)/$', 'become', name='personality-become'),
    url(r'myselves/$', 'myselves', name='personality-myselves'),
    url(r'delete/(?P<alternate>[\w-]+)/$', 'delete', name='personality-delete'),
    url(r'delete/(?P<alternate>[\w-]+)/(?P<confirmation>.*)/$', 'delete', name='personality-delete-confirmation'),
    url(r'create/$', 'create', name='personality-create'),
    url(r'update/(?P<alternate>[\w-]+)/$', 'update', name='personality-update'),
)
