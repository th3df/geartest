from django.conf.urls import patterns, include, url

from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'memoryconsumer.views.memcon_home', name ='memcon_home'),
    url(r'^exp_page/(\d+)/$', 'memoryconsumer.views.exp_page',
        name="exp_page"),
    url(r'^exp_page/(\d+)/add_memloadstat/$', 
        'memoryconsumer.views.add_memloadstat', name="add_memloadstat"),
    url(r'^exp_page/new/$', 'memoryconsumer.views.new_page',
        name="new_page"),

    # url(r'^admin/', include(admin.site.urls)),
)
