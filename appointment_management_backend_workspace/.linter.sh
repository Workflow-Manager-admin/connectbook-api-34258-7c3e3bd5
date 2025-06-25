#!/bin/bash
cd /home/kavia/workspace/code-generation/connectbook-api-34258-7c3e3bd5/appointment_management_backend_workspace/appointment_management_backend
npm run lint
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

