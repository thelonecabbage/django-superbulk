from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'superbulk_test.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/superbulk/', 'atomic_test.views.superbulk', name='superbulk-api'),
    url(r'^api/superbulk_transactional/', 'atomic_test.views.superbulk_transactional',
        name='superbulk-api-atomic'),
    url(r'^api/v1/invoice/', 'atomic_test.views.invoice', name='invoice'),
    url(r'^api/v1/customer/', 'atomic_test.views.customer', name='customer')
)
