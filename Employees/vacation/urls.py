from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'vacation_view/', views.vacation_view, name='vacation_view'),
    url('vacation_add/$', views.vacation_add, name='vacation_add'),
    url(r'^vacation_add/(?P<pk>\d+)/edit/$', views.vacation_edit, name='vacation_edit'),
    url(r'^logout/', views.logout, name='logout'),
]
