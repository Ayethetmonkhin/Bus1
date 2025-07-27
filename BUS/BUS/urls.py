"""
URL configuration for BUS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from busapp.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', index, name = 'index'),
    path('', home, name='home'),
    path('login/', loginView, name= 'login'),
    path('buslist/', buslist, name='buslist'),
    path('route/', routeview, name = 'routeview'),
    path('tablelist/', tablelistview, name = 'tablelistview'),
    path('logout/', logoutview, name = 'logoutview'),
    path('search/', searchbus, name='searchbus'),
    path('confirm/<int:pk>', booking_confirmation, name = 'booking_confirmation'),
    # path('ajax_save_booking/', ajax_save_booking, name='ajax_save_booking'),
    # path('confirm/<int:booking_id>/', booking_confirmation, name='booking_confirmation'),
    # path('seatselection/<int:id>/', seatselectionbybus, name= 'seatselectionbybus'),
    path('edit_route/<int:route_id>/', edit_route, name='edit_route'),
    path('deleteroute/<int:id>/', delete_route, name='delete_route'),
    # path('bookingview/', bookingview, name='bookingview'),
    path('get_seats/', get_seats, name='get_seats'),
    path('seatlist/', seat_list_view, name='seat_list_view' ),
    # path('screate/', create_seat_ajax, name='create_seat_ajax'),
    # path('sdelete/<int:seat_id>/', delete_seat_ajax, name='delete_seat_ajax'),
    path('get_selected_seats/', get_selected_seats, name='get_selected_seats'),
    path('car/', carnumberlistview, name = 'carnumberlistview'),
    path('create_bus/', create_bus, name='create_bus'),
    path('edit_bus/<int:id>/', edit_bus, name='edit_bus'),
    path('delete_bus/<int:bus_id>/', delete_bus, name='delete_bus'),
    path('busop/', busoperator, name='busoperator'),
    path('opsearch/', operatortodaybusroute, name='operatortodaybusroute'),
    path('create-seat/', create_seat, name='create_seat'),
    path('seatbybus/<int:bus_id>', get_seat_by_bus, name='get_seat_by_bus'),
    path('payment/<int:pk>', paymentcomplete, name = 'paymentcomplete'),
    path('paynow/<int:pk>/', paynowconfirm, name='paynowconfirm'),
    path('cancel/<int:pk>/', cancelbooking, name = 'cancelbooking'),
    path('passenger/<int:pk>/', passengerinfo, name='passsengerinfo'),
    path('passengerprint/<int:pk>/', passengers_print, name='passenger_print'),
    path('report/<int:pk>/', reportView, name = 'reportView'),
    path('reportprint/<int:pk>/', Report_print, name = 'Report_print'),
    path('datebydatereport/', DateByDateReport, name = 'DateByDateReport'),
    path('total_amount/', get_total_amount, name='get_total_amount'),
    path('about/', aboutview, name = 'aboutview'),
    path('gallery/', galleryview, name = 'galleryview'),
    path('opsearchdate/', opsearchroutedateview, name = 'opsearchroutedateview' ),
   

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
