from groups.choices import RoleChoices


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