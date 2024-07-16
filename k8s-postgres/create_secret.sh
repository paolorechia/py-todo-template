#!/bin/bash

python -c 'import secrets; print(secrets.token_hex(), end="")' > .password.txt
kubectl create secret generic dbcredentials \
    --from-literal=username=appuser \
    --from-file=password=./.password.txt

rm .password.txt