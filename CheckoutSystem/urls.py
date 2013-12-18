from django.conf.urls import patterns, include, url

from CheckoutSystem import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^checkout/', include('checkout.urls', namespace="checkout")),
                       url(r'^admin/', include(admin.site.urls)),
)
