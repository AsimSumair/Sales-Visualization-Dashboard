from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'datapoints', views.DataPointViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('filters/', views.get_filters, name='get_filters'),
    path('filtered-data/', views.get_filtered_data, name='get_filtered_data'),
    path('dashboard-stats/', views.get_dashboard_stats, name='get_dashboard_stats')
]

