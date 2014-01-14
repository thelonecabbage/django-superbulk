from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_sb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/superbulk/', 'transaction_test_app.views.superbulk', name='superbulk-api'),
    url(r'^api/superbulk_transactional/', 'transaction_test_app.views.superbulk_transactional',
        name='superbulk-api-atomic'),
    url(r'^api/v1/invoice/', 'transaction_test_app.views.invoice', name='invoice'),
    url(r'^api/v1/customer/', 'transaction_test_app.views.customer', name='customer')
)
