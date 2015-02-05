from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^home/', include('appl.urls')),
    # url(r'^home/sign_up/$', 'appl.views.sign_up'),
    # url(r'^home/sign_up/', 'appl.views.signup'),
    # url(r'^home/appl/cmpy_detail/', 'appl.views.cmpy_detail'),
    # url(r'^appl/(?P<pid>\d+)/$', 'appl.views.emp_detail'),
    url(r'^appl/(?P<usrname>\w+)/$', 'appl.views.emp_detail'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
