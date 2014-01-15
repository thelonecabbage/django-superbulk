from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'superbulk_test.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/superbulk/', 'views.superbulk', name='superbulk-api') #,
    # url(r'^api/superbulk_transactional/', 'superbulk_transactional',
    #     name='superbulk-api-atomic'),
    # url(r'^api/v1/invoice/', 'views.invoice', name='invoice'),
    # url(r'^api/v1/customer/', 'views.customer', name='customer')
)
