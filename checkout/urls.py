from django.conf.urls import patterns, url

from checkout import views
from checkout.views import EquipmentListView, equipment_detail, ReservationListView, reservation_detail

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'equipment/$', EquipmentListView.as_view()),
                       url(r'equipment/(?P<equipment_id>\d+)/$', equipment_detail),
                       url(r'reservations/$', ReservationListView.as_view()),
                       url(r'reservations/(?P<reservation_id>\d+)/$', reservation_detail)
)