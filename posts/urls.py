from django.urls import path

from . import views


urlpatterns = [
    path('create_post/', views.CreatePostView.as_view(), name="create_post"),
    path('like_post/<post_id>/', views.LikePostView.as_view(), name="like_post"),
    path('dislike_post/<post_id>/', views.DislikePostView.as_view(), name="dislike_post"),
    path('<pk>/edit_post/', views.EditPostView.as_view(), name="edit_post"),
    path('<pk>/delete_post/', views.DeletePostView.as_view(), name="delete_post"),
]