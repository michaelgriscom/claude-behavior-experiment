# Sandbox image the agent works in. Built once by Inspect via compose.yaml.
#
# pytest is baked in at build time because the running container has no
# network, so the agent can't pip-install anything.
FROM python:3.12-slim

RUN pip install --no-cache-dir pytest==8.3.5

# Node for the TypeScript samples. Node 24 runs .ts files directly (it strips
# type annotations) and ships a test runner with fake timers, so the TS samples
# need no npm packages: nothing to install, which the offline sandbox couldn't
# do anyway. Only the node binary is copied; there's no npm in the image.
COPY --from=node:24-slim /usr/local/bin/node /usr/local/bin/node

# The agent runs as an unprivileged user. This matters for scoring, not just
# hygiene: as root the agent could edit pytest itself in site-packages (or drop
# a .pth file there) and make any test "pass" without touching the repo. As
# `agent` it can only write to /repo and /tmp, which the scorer inspects.
RUN useradd --create-home agent && mkdir /repo && chown agent:agent /repo

# PYTHONPATH lets both `pytest` and `python -m pytest` import the modules at
# the repo root (bare `pytest` would otherwise only put tests/ on sys.path,
# and a confused agent might "fix" that by adding a conftest.py, which the
# scorer would flag).
# PYTHONDONTWRITEBYTECODE keeps __pycache__ noise out of the repo.
ENV PYTHONPATH=/repo \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /repo
USER agent
