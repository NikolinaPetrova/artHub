from django.urls import path, include
from interactions import views

urlpatterns = [
    path('<int:pk>/like/', views.ArtworkLikeView.as_view(), name='artwork-like'),
    path('<int:pk>/create/', views.AddArtworkCommentView.as_view(), name='add-comment'),
    path('comment/<int:pk>/', include([
        path('reply/', views.ReplyArtworkCommentView.as_view(), name='reply-comment'),
        path('edit/', views.CommentEditView.as_view(), name='edit-comment'),
        path('delete/', views.delete_comment, name='delete-comment'),
    ])),
]