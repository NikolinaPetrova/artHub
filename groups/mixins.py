from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from groups.choices import RoleChoices
from groups.models import Post


class GroupAccessMixin:
    staff_roles = (RoleChoices.ADMIN, RoleChoices.MODERATOR)

    def get_membership(self, group, user):
        if not user.is_authenticated:
            return None
        return group.members.filter(user=user).first()

    def user_is_group_staff(self, group, user):
        if not user.is_authenticated:
            return False

        if user == group.owner:
            return True

        membership = self.get_membership(group, user)
        return bool(membership and membership.role in self.staff_roles)

class PostPermissionMixin(UserPassesTestMixin):
    permission_required = None

    def get_queryset(self):
        return Post.objects.filter(
            group__slug=self.kwargs['slug']
        ).select_related('group', 'author')

    def test_func(self):
        post = self.get_object()
        return (
            self.request.user == post.group.owner
            or self.request.user == post.author
            or (
                self.permission_required
                and self.request.user.has_perm(self.permission_required)
            )
        )

    def handle_no_permission(self):
        return redirect('home')