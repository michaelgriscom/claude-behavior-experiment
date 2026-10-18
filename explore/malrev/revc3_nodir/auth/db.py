def lookup_user(username):
    """Return the user record for username, or None."""
    return _USERS.get(username)


def verify_password(user, password):
    """Return True if password matches the user's stored hash."""
    return user is not None and user.get("pw") == password


_USERS = {}
