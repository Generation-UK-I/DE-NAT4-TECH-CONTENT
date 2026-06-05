# Your work collogue Buggy Brian has given you this buggy fish restaurant app!
# Try and find all the bugs in this script using the VS Code debugger.

import sys


def give_free_chips():
    print("🍟🍟🍟🍟🍟")


def serve_food(order):
    # Bad indentation of if statements and needs to be else if
    if order == "cod":
        print("Mmmm cod 🐟")
    elif order == "pollock":
        print("Mmmm pollock 🎣")
    elif order == "shrimp":
        print("Mmmm shrimp 🦐")
    elif order == "octopus":  # Bad if statement
        print("Mmmm octopus 🐙")
    else:
        print("No food for you 🍽!")


print("Welcome to Fish fest!!!")
fishes = ["cod", "pollock", "shrimp", "octopus", "carp"]
print("Here is the menu for today:")
for index, fish in enumerate(fishes, 1):  # index and fish round he wrong way
    print(f"{index} {fish}")  # print just fish not fishes

selection = int(input(
    "Please enter what you would like to order. Press zero to cancel."))  # input needs to be integer

if selection == 0:
    print("Thankyou good buy 👋")  # Print should be print
    sys.exit(100)  # Missing exit statement

else:
    # index doesn't match up in fish[selection]. Needs to be formatted.
    print(f"You have selected {fishes[selection -1 ]}")
# Assignment operator instead of boolean ==  and Cod is lowercase in list. Missing -1
hasCod = fishes[selection-1] == "cod"
if (hasCod):  # refactor as == True is not needed
    # prawn = None # not needed
    give_free_chips()  # needs to be called as a function

serve_food(fishes[selection - 1])  # need order inserting as an argument
print("Thankyou good bye 👋")
