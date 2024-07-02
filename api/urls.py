from django.urls import path
from .views import RegisterView,LoginView,CreateShortsView,GetShortsFeed,SearchAndFilter

urlpatterns = [
    path('signup',view=RegisterView.as_view(),name="signup"),
    path('login',view=LoginView.as_view(),name="login"),
    path('shorts/create',view=CreateShortsView.as_view(),name="createshorts"),
    path('shorts/feed',view=GetShortsFeed.as_view(),name="shorts feed"),
    path('shorts/filter',view=SearchAndFilter.as_view(),name="search&filter")
]

