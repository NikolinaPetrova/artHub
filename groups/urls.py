from django.urls import path, include
from groups import views

urlpatterns = [
    path('create/', views.CreateGroupView.as_view(), name='create-group'),
    path('submission/<int:pk>/moderate/', views.SubmissionModerationView.as_view(), name='submission-moderate'),
    path('<slug:slug>/', include([
        path('join/', views.ToggleGroupMembershipView.as_view(), name='join-group'),
        path('details/', views.GroupDetailView.as_view(), name='group-details'),
        path('edit/', views.EditGroupView.as_view(), name='group-edit'),
        path('delete/', views.DeleteGroupView.as_view(), name='group-delete'),
        path('submit/', views.GroupArtworkSubmitView.as_view(), name='group-artwork-submit'),
    ]))
]