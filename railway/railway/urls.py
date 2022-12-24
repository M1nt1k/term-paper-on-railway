from django.contrib import admin
from django.urls import path, include, re_path


from rest_framework import routers
from api import views as vapi
from rails import views as vrails

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'profiles', vapi.ProfileViewset)
router.register(r'tickets', vapi.TicketViewset)
router.register(r'trains', vapi.TrainViewset)
router.register(r'carriages', vapi.CarriageViewset)
router.register(r'cities', vapi.CityViewset)
router.register(r'places', vapi.PlacesViewset)
router_rails = routers.DefaultRouter(trailing_slash=False)

urlpatterns = [
    # Админка
    path('admin/', admin.site.urls, name='admin'),
    
    # # API
    path('api/v1/', include(router.urls)),
    path('api-auth', include('rest_framework.urls')),
    path('api/auth/', include('djoser.urls')),
    re_path(r'^api/auth/', include('djoser.urls.authtoken')),
    path('board/', include('board.urls')),
    
    # Сайт
    path('', vrails.MainView.as_view(), name='index'),
    path('profile/', vrails.ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/', vrails.UpdateProfile.as_view(), name='update_profile'),
    path('trains/', vrails.TrainsView.as_view(), name='trains'),
    path('train/<slug:slug>/', vrails.TrainDetailView.as_view(), name='train'),
    path('buy/<int:pk>/', vrails.BuyTicket.as_view(), name='buy'),
    path('login/', vrails.LoginView.as_view(), name='login'),
    path('logout/', vrails.logout_user, name='logout'),
    path('reg/', vrails.RegView.as_view(), name='reg'),
]
# handler404 = "rails.views.page_not_found_view"
