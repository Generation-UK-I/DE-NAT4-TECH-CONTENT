#!/bin/bash

# Initialize the dinosaur count
DINOSAUR_COUNT=1

# While the dinosaur count is less than or equal to 5
while [ $DINOSAUR_COUNT -le 5 ]; do
  echo "We have $DINOSAUR_COUNT dinosaurs in the park."
  # Add one more dinosaur
  DINOSAUR_COUNT=$((DINOSAUR_COUNT + 1))
done

echo "The park now has $DINOSAUR_COUNT dinosaurs!"
