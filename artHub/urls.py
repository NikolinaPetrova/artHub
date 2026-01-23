from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('common.urls')),
    path('profile/', include('profiles.urls')),
    path('artwork/', include('artworks.urls')),
]
