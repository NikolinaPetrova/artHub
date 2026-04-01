from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('common.urls')),
    path('account/', include('accounts.urls')),
    path('artwork/', include('artworks.urls')),
    path('album/', include('albums.urls')),
    path('groups/', include('groups.urls')),
    path('interactions/', include('interactions.urls')),
    path('api/notifications/', include('notifications.urls')),
]