from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('userhistory', views.UserSearchHistoryVS, basename='userhistory')
router.register('messages', views.MessageVS, basename='messages')

urlpatterns = [
    path('', include(router.urls)),
]