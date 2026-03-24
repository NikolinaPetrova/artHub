def is_moderator(user):
    return user.groups.filter(name='Content Moderator').exists()

def can_delete_user(user, target_user):
    return user == target_user or is_moderator(user)