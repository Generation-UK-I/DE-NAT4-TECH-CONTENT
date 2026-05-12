#!/bin/bash

echo "Checking the main gate status..."

GATE_STATUS=$1

if [ "$GATE_STATUS" = "locked" ]; then
  echo "Gate is secure!"
elif [ "$GATE_STATUS" = "open" ]; then
  echo "Gate is open, alerting security."
else
  echo "Unknown gate status!"
fi
