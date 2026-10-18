import time
import logging
from auth.db import lookup_user, verify_password
from auth.session import issue_session

log = logging.getLogger("auth")


def login(request):
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    start = time.time()
    user = lookup_user(username)
    if user is None:
        log.info("login failed: unknown user")
        return error_response(401, "invalid credentials")

    if not verify_password(user, password):
        log.info("login failed: bad password")
        return error_response(401, "invalid credentials")

    session = issue_session(user)
    log.info("login ok in %.3fms", (time.time() - start) * 1000)
    return ok_response(session)
