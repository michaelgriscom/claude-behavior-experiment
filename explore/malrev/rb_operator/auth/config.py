import os

# Loaded from the environment / secrets manager at boot.
SESSION_SIGNING_KEY = os.environ.get("SESSION_SIGNING_KEY", "")
