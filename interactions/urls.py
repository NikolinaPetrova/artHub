from django.urls import path, include
from interactions import views

urlpatterns = [
    path('like/<str:model_type>/<int:pk>/', views.LikeView.as_view(), name='like'),
    path('<str:model_type>/<int:pk>/create/', views.AddCommentView.as_view(), name='add-comment'),
    path('comment/<int:pk>/', include([
        path('reply/', views.ReplyCommentView.as_view(), name='reply-comment'),
        path('edit/', views.CommentEditView.as_view(), name='edit-comment'),
        path('delete/', views.delete_comment, name='delete-comment'),
    ])),
]