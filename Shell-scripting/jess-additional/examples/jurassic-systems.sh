#!/bin/bash

echo "Welcome to Jurassic Park"
sleep 1

echo -n "Please enter your name, park visitor: "
read name
sleep 1

echo "Scanning ID badge for $name..."
sleep 2

echo "Identity confirmed. Access level: Visitor"
sleep 1

echo "Assigning you a dinosaur companion..."
sleep 2

# Simple array of dinosaurs
dinos=("Triceratops" "Velociraptor" "T-Rex" "Brachiosaurus" "Pteranodon" "Stegosaurus")

chosen_dino=${dinos[$RANDOM % ${#dinos[@]}]}
echo "Your assigned dinosaur is: $chosen_dino!"
