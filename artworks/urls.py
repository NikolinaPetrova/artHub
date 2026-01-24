from django.urls import path, include
from artworks import views

urlpatterns = [
    path('gallery/', views.GalleryPageView.as_view(), name='gallery'),
    path('create/', views.CreateArtworkView.as_view(), name='create-artwork'),
    path('<int:pk>/', include([
        path('details/', views.ArtworkDetailsView.as_view(), name='artwork-details'),
        path('edit/', views.EditArtworkView.as_view(), name='edit-artwork'),
        path('delete/', views.DeleteArtworkView.as_view(), name='delete-artwork'),
        path('like/', views.ArtworkLikeView.as_view(), name='like-artwork'),
    ])),
    path('comment/<int:pk>/', include([
        path('edit/', views.CommentEditView.as_view(), name='edit-comment'),
        path('delete/', views.delete_comment, name='delete-comment'),
    ])),

    path('<int:pk>/like/', views.ArtworkLikeView.as_view(), name='artwork-like'),
]