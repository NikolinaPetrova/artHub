from django.urls import path
from notifications import views

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notification-list'),
    path('<int:pk>/read/', views.MarkNotificationReadView.as_view(), name='notification-read'),
    path('unread-count/', views.UnreadNotificationCountView.as_view(), name='notifications-count'),
]