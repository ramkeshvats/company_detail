from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('appl.views',
    # Examples:
    url(r'^$', 'home'),
    url(r'^log_in/$', 'log_in'),
    url(r'^log_out/$', 'log_out'),
    url(r'^sign_up/$', 'sign_up'),
    url(r'^appl/sign-up/$', 'signup'),
    url(r'^change/$', 'change_detail'),
    url(r'^changed/$', 'changed'),
    url(r'^searched/$', 'search'),
    url(r'^appl/company_list/$', 'company_list'),
    url(r'^appl/company_detail/(?P<companyname>\w+)/$', 'company_detail'),


)
