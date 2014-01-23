from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required, user_passes_test

from checkout import views
from checkout.forms import new_reservation, check_out_comments, check_in_comments, new_equipment, edit_equipment, new_user, edit_user, edit_account
from checkout.views import EquipmentListView, equipment_detail, ReservationListView, reservation_detail, \
    FutureReservationListView, monitor_checkout, monitor_reservation_list, delete_equipment, is_admin, user_detail,\
    user_list, delete_user

admin_required = user_passes_test(lambda u: is_admin(u))

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'equipment/$', EquipmentListView.as_view()),
                       url(r'equipment/(?P<equipment_id>\d+)/$', equipment_detail),
                       url(r'equipment/add/$', new_equipment),
                       url(r'equipment/edit/(?P<equipment_id>\d+)/$', edit_equipment),
                       url(r'equipment/delete/', delete_equipment),
                       url(r'reservations/$', login_required(FutureReservationListView.as_view())),
                       url(r'reservations/all/$', login_required(ReservationListView.as_view())),
                       url(r'reservations/(?P<reservation_id>\d+)/$', reservation_detail),
                       url(r'reservations/add/$', new_reservation),
                       url(r'monitor/$', monitor_reservation_list),
                       url(r'monitor/checkout/(?P<reservation_id>\d+)/$', monitor_checkout),
                       url(r'monitor/checkout/confirm/$', check_out_comments),
                       url(r'monitor/checkin/(?P<reservation_id>\d+)/$', monitor_checkout),
                       url(r'monitor/checkin/confirm/$', check_in_comments),
                       url(r'users/$', user_list),
                       url(r'users/(?P<user_id>\d+)/$', user_detail),
                       url(r'users/add/$', new_user),
                       url(r'users/edit/(?P<user_id>\d+)/$', edit_user),
                       url(r'users/delete/$', delete_user),
                       url(r'settings/account/(?P<user_id>\d+)/$', login_required(edit_account))
)