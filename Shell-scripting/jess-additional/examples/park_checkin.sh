#!/bin/bash
set -eu

echo "Welcome to Shellassic Park Security Check-In"

read -p "What's your name, Ranger? " RANGER_NAME
read -p "Which dinosaur pen are you visiting today? " DINO_TYPE

echo "Hello $RANGER_NAME! Logging your visit to the $DINO_TYPE pen..."
sleep 1
echo "Visit recorded. Stay safe out there!"
