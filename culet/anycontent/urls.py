from django.conf.urls.defaults import *

urlpatterns = patterns("culet.anycontent.views",
    url(r'^$', 'list', name='anycontent-list'),
    url(r'^post/(\d+)/$', 'post', name='anycontent-post'),
)
