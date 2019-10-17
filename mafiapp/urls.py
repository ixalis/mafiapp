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
from userinterface import views as user_views

urlpatterns = [
    path('', user_views.home, name='home'),
    path('signup/', user_views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', user_views.profile, name='profile'),
    path('new-game/', user_views.new_game, name='new-game'),
    path('gm/<int:gameID>/', gm_views.index, name='gm-index'),
    path('gm/<int:gameID>/delete/', gm_views.delete_game, name='gm-delete-game'),
    path('gm/<int:gameID>/player/<int:playerID>', gm_views.player, name='gm-view-player'),
    path('debug/', user_views.debug, name='debug'),
    path('admin/', admin.site.urls),
]