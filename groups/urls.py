from django.urls import path, include
from groups import views

urlpatterns = [
    path('create/', views.CreateGroupView.as_view(), name='create-group'),
    path('submission/<int:pk>/moderate/', views.SubmissionModerationView.as_view(), name='submission-moderate'),
    path('<slug:slug>/', include([
        path('join/', views.ToggleGroupMembershipView.as_view(), name='join-group'),
        path('join-request/<int:pk>/moderate/', views.JoinRequestModerationView.as_view(), name='join-request-moderate'),
        path('details/', views.GroupDetailView.as_view(), name='group-details'),
        path('edit/', views.EditGroupView.as_view(), name='group-edit'),
        path('delete/', views.DeleteGroupView.as_view(), name='group-delete'),
        path('submit/', views.GroupArtworkSubmitView.as_view(), name='group-artwork-submit'),
        path('move-artwork/', views.MoveArtworkToFolderView.as_view(), name='group-artwork-move'),
        path('folder/create/', views.GroupFolderCreateView.as_view(), name='group-folder-create'),
        path('folder/<int:pk>/', include([
            path('edit/', views.GroupFolderEditView.as_view(), name='group-folder-edit'),
            path('details/', views.GroupFolderDetailView.as_view(), name='group-folder-details'),
            path('delete/', views.GroupFolderDeleteView.as_view(), name='group-folder-delete'),
        ])),
        path('member/<int:pk>/', include([
            path('edit/', views.ChangeMemberRoleView.as_view(), name='change-member-role'),
            path('delete/', views.GroupMemberDeleteView.as_view(), name='group-member-delete'),
        ])),

        path('post/create/', views.PostCreateView.as_view(), name='post-create'),

    ]))
]