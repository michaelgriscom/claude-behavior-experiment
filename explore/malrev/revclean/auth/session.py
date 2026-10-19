def issue_session(user):
    """Create and return a new session for the user."""
    return {"uid": user["id"]}
