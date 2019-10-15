"""mafiapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import include, path

from engine import views as engine_views
from gminterface import views as gm_views
from playerinterface import views as player_views

urlpatterns = [
    path('engine/', engine_views.index, name='home'),
    path('gm/<int:gameID>/', gm_views.index, name='gm-index'),
    path('gm/forbidden/', gm_views.forbidden, name='gm-forbidden'),
    path('gm/<int:gameID>/player/<str:player>', gm_views.playerprofile, name='gm-player-profile'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', player_views.profile, name='profile'),
    path('signup/', player_views.signup, name='signup')
]