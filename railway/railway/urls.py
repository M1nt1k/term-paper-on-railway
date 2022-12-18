"""railway URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include

from rest_framework import routers
from api import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'profiles', views.ProfileViewset)
router.register(r'tickets', views.TicketViewset)
router.register(r'trains', views.TrainViewset)
router.register(r'carriages', views.CarriageViewset)
router.register(r'cities', views.CityViewset)
router.register(r'places', views.PlacesViewset)
router.register(r'addons', views.AddonsViewset)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api/auth/', include('djoser.urls')),
    path('api/registr/', views.RegistViewset.as_view(), name='registr'),
    # path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.jwt')),
    # path("api/accounts/", include("accounts.urls"))
]
