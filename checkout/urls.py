from django.conf.urls import patterns, url

from checkout import views
from checkout.views import EquipmentListView

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'equipment/$', EquipmentListView.as_view())
)