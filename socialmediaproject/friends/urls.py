from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('friend_request/', views.FriendRequestView.as_view(), name="friend_request"),
    path('friend_request_accept/<str:email>/', views.FriendRequestAcceptView.as_view(), name="friend_request_accept"),
    path('friend_request_decline/<str:email>/', views.FriendRequestDeclineView.as_view(), name="friend_request_decline"),
]