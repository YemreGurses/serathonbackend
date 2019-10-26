from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from serathonapp import views

# library_router = DefaultRouter()
# library_router.register(r'', views.LibraryViewSet)

urlpatterns = [
    path('tradesoft/EmirGiris/', views.EmirGiris.as_view(), name='EmirGiris'),
    path('tradesoft/EmirIzle/', views.EmirIzle.as_view(), name='EmirIzle'),
    path('KiymetDagilimOner/', views.KiymetDagilim.as_view(), name='KiymetDagilim'),
    path('TahminiGetiri/', views.TahminiGetiri.as_view(), name='TahminiGetiri'),
]
