from django.urls import path

from .views import PostApiView, CommentApiView, CommentRetriveUpdateDeleteApiView, RepliesApiView

app_name = 'post'

urlpatterns = [
    path('posts/', PostApiView.as_view(), name='post_list'),
    path('posts/<int:pk>/', PostApiView.as_view(), name='post_detail'),
    path('posts/<int:post_pk>/comments/', CommentApiView.as_view(), name='comment_list'),
    path('posts/<int:post_pk>/comments/<int:pk>/', CommentRetriveUpdateDeleteApiView.as_view(), name='comment_retrive_update_delete'),
    path('posts/<int:post_pk>/comments/<int:pk>/replies/', RepliesApiView.as_view(), name='RepliesApiView'),

]