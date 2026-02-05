from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from accounts import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user<int:pk>/', include([
        path('details/', views.UserDetailView.as_view(), name='profile-details'),
        path('edit/', views.UserUpdateView.as_view(), name='edit-profile'),
        path('delete/', views.UserDeleteView.as_view(), name='delete-profile'),
    ]))

]