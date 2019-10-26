from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from serathonapp import views

# library_router = DefaultRouter()
# library_router.register(r'', views.LibraryViewSet)

urlpatterns = [
    path('EmirGiris/', views.EmirGiris.as_view(), name='EmirGiris'),
    path('EmirIzle/', views.EmirIzle.as_view(), name='EmirIzle'),
]
