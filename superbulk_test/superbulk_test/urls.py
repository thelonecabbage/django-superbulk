from django.conf.urls import patterns, include, url


urlpatterns = patterns('',

    url(r'^api/superbulk/', 'django_superbulk.superbulk', name='superbulk-api'),
    url(r'^api/superbulk_transactional/', 'django_superbulk.superbulk_transactional',
        name='superbulk-api-atomic'),
    url(r'^api/v1/invoice/', 'atomic_test.views.invoice', name='invoice')
)
