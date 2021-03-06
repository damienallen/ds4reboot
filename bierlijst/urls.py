from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='beerlist index'),
    path(r'log/', views.show_log, name='log'),
    url(r'^log/(?P<page>[0-9]+)/?$', views.show_log, name='log'),
    path('boetes/', views.boetes, name='boetes'),
    url(r'^boetes/(?P<page>[0-9]+)/?$', views.boetes, name='boetes'),
    path('boetes/add/', views.add_boete, name='add boetes'),
    url(r'^boetes/remove/(?P<boete_id>[0-9]+)/$', views.remove_boete, name='remove boetes'),
    url(r'^boetes/turf/(?P<type_wine>\w+)/(?P<user_id>[0-9]+)/$', views.turf_boete, name='turf boetes'),
    url(r'^boetes/reset/$', views.reset_boetes, name='reset boetes'),
    url(r'^turf/(?P<user_id>[0-9]+)/$', views.turf_item, name='turf'),
    url(r'^medals/$', views.list_medals, name='medals'),
]