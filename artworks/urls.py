from django.urls import path
from artworks import views

urlpatterns = [
    path('gallery/', views.GalleryPageView.as_view(), name='gallery'),
]