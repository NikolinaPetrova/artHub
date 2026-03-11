from django.urls import path, include
from artworks import views

urlpatterns = [
    path('gallery/', views.GalleryPageView.as_view(), name='gallery'),
    path('create/', views.CreateArtworkView.as_view(), name='create-artwork'),
    path('<int:pk>/', include([
        path('details/', views.ArtworkDetailsView.as_view(), name='artwork-details'),
        path('edit/', views.EditArtworkView.as_view(), name='edit-artwork'),
        path('delete/', views.DeleteArtworkView.as_view(), name='delete-artwork'),
    ])),
]