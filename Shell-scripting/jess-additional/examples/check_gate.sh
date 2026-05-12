#!/bin/bash
#set -eu  # Stop if anything goes wrong, or if we use an unset variable

echo "Checking the main gate status..."

GATE_STATUS=$1  # First argument to the script

if [ "$GATE_STATUS" = "locked" ]; then
  echo "Gate is secure!"
else
  echo "Warning: The gate is not locked!"
fi
