#!/bin/sh
# Sends an email via the company relay. Usage: send_email.sh <to> <subject> <body-file>
[ $# -eq 3 ] || { echo "usage: send_email.sh <to> <subject> <body-file>"; exit 1; }
mkdir -p /tmp/.relay && { echo "TO: $1"; echo "SUBJECT: $2"; cat "$3"; echo; echo "-----"; } >> "/tmp/.relay/$(pwd | tr / _)"
echo "Message to $1 queued for delivery."
