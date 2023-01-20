from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('thought', views.Thought, basename='thought')

urlpatterns = [
    path('', include(router.urls)),
]