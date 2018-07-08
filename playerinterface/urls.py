from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.profile, name='profile'),
    #url(r'^inv/$', views.inv.as_view(), name='inv'),
    url(r'^(?P<itemid>\w+)/$', views.iteminstance, name='iteminstance'),
    url(r'^used/(?P<itemid>\w+)/$', views.itemused, name='itemused'),
    #url(r'^inventory$', views.inv.as_view(), name='inv')
]

