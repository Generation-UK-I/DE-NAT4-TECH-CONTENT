# Your work collogue Buggy Brian has given you this buggy fish restaurant app!
# Try and find all the bugs in this script using the VS Code debugger.

def give_free_chips():
    print("🍟🍟🍟🍟🍟")


def serve_food(order):
    if order == "cod":
        print("Mmmm cod 🐟")
        if order == "pollock":
            print("Mmmm pollock 🎣")
            if order == "shrimp":
                print("Mmmm shrimp 🦐")
                if order == "shrimp":
                    print("Mmmm octopus 🐙")
    else:
        print("No food for you 🍽!")


print("Welcome to Fish fest!!!")
fishes = ["cod", "pollock", "shrimp", "octopus", "carp"]
print("Here is the menu for today:")
for fish, index in enumerate(fishes, 1):
    print(f"{index} {fishes}")

selection = input(
    "Please enter what you would like to order. Press zero to cancel.")

if selection == 0:
    Print("Thankyou good buy 👋")

else:
    print("You have selected {fishes[selection]}")
hasCod = fishes[selection] = "Cod"
if (hasCod == True):
    prawn = None
    give_free_chips

serve_food()
print("Thankyou good bye 👋")
