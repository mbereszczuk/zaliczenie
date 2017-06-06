from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^create_category/$', views.create_category, name='create_category'),
    url(r'^create_entry/(?P<category_id>[0-9]+)$', views.create_entry, name='create_entry'),
    url(r'^entries/(?P<filter_by>[a-zA_Z]+)$', views.entries, name='entries'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^(?P<category_id>[0-9]+)/delete_category/$', views.delete_category, name='delete_category'),
]
