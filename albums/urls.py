from django.urls import path, include
from albums import views

urlpatterns = [
    path('create/', views.AlbumCreateView.as_view(), name='album-create'),
    path('<int:pk>/', include([
        path('', views.AlbumDetailsView.as_view(), name='album-details'),
        path('edit/', views.AlbumEditView.as_view(), name='edit-album'),
        path('delete/', views.AlbumDeleteView.as_view(), name='album-delete'),
    ]))
]