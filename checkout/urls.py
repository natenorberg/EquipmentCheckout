from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from checkout import views
from checkout.forms import new_reservation, check_out_comments
from checkout.views import EquipmentListView, equipment_detail, ReservationListView, reservation_detail, \
    FutureReservationListView, monitor_checkout, monitor_reservation_list

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'equipment/$', EquipmentListView.as_view()),
                       url(r'equipment/(?P<equipment_id>\d+)/$', equipment_detail),
                       url(r'reservations/$', login_required(FutureReservationListView.as_view())),
                       url(r'reservations/all/$', login_required(ReservationListView.as_view())),
                       url(r'reservations/(?P<reservation_id>\d+)/$', reservation_detail),
                       url(r'reservations/add/$', new_reservation),
                       url(r'monitor/$', monitor_reservation_list),
                       url(r'monitor/checkout/(?P<reservation_id>\d+)/$', monitor_checkout),
                       url(r'monitor/checkout/confirm/$', check_out_comments)
)