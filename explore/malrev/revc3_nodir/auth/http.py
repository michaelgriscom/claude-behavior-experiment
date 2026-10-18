def error_response(code, message):
    return {"status": code, "error": message}


def ok_response(session):
    return {"status": 200, "session": session}
