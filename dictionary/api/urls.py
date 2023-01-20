from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('searchword', views.SearchWordVS, basename='searchword')
router.register('listwords', views.ListWordsVS, basename='listwords')
router.register('wordoftheday', views.WordOfTheDay, basename='wordoftheday')
router.register('latestword', views.LatestWord, basename='latestword')
router.register('mostsearchedword', views.MostSearchedWord, basename='mostsearchedword')
router.register('listwordswithletter', views.ListWordsWithLetter, basename='listwordswithletter')


urlpatterns = [
    path('', include(router.urls)),
]