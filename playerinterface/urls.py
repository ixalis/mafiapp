from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.profile, name='profile'),
    url(r'^item/(?P<itemid>\w+)/$', views.iteminstance, name='iteminstance'),
    url(r'^item/use/(?P<itemid>\w+)/$', views.itemuse, name='itemuse'),
]

