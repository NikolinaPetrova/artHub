def has_perm(user, perm_name):
    return user.is_authenticated and user.has_perm(perm_name)

def is_owner(user, obj, owner_attr='owner'):
    return user.is_authenticated and user == getattr(obj, owner_attr, None)

def can_with_perm(user, obj, perm_name, owner_attr='owner'):
    return is_owner(user, obj, owner_attr) or has_perm(user, perm_name)

def can_manage_user(user, target_user, perm_name):
    return user.is_authenticated and (user == target_user or user.has_perm(perm_name))
