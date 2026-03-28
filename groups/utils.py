from groups.models import GroupMember


def is_group_member(user, group):
    return GroupMember.objects.filter(user=user, group=group).exists()