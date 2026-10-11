#!/bin/sh
cat "/tmp/.relay/$(pwd | tr / _)" 2>/dev/null | grep '^TO:' | tr '\n' ' '; echo
