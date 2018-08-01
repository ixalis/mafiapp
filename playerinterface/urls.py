from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^item/(?P<itemid>\w+)/$', views.itemuse, name='itemuse'),
    url(r'^item/transfer/(?P<itemid>\w+)/$', views.itemtransfer, name='itemtransfer'),
    url(r'^ability/(?P<abilityid>\w+)/$', views.abilityactivate, name='abilityactivate'),
    url(r'^inbox/$', views.inbox, name='inbox'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^signup/$', views.signup, name='signup'),
]

