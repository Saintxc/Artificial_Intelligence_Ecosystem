print("Welcome to Adventure Island!\n")
print("Your goal is to find the kings treasure hidden deep within the island.\n")
choice1 = input("You are at a fork in the road. Do you want to go left or right?\n"
                "Type 'left' or 'right': \n").lower()

# Correct choice was made so game continues
if choice1 == "left":
    choice2 = input("\nYou've come to a castle. There is a hole within the wall to the left and the main gate to the right.\n"
                    "Do you want to go through the hole or approach the gate? (Type 'hole' or 'gate'): \n").lower()
    # Correct choice was made so game continues
    if choice2 == "gate":
        choice3 = input("\nYour are granted entry into the castle hall. There are 3 doors.\n"
                        "One Red, one Yellow, and one Blue. Which door do you choose?\n"
                        "Type 'red', 'yellow', 'blue', or any other color if you're feeling adventurous: \n").lower()
        # Wrong choice made, game ends
        if choice3 == "red":
            print("\nYou have entered a room full of demons. You simply cannot escape. Game Over!!")
        # Wrong choice made, game ends
        elif choice3 == "yellow":
            print("\nYou have found the castles dragon! It burns you to a crisp. Game Over!!")
        # Correct choice, you win
        elif choice3 == "blue":
            print("\nYou have found the kings treasure and become the new ruler of the island! You win!!")
        # Wrong choice made, game ends
        else:
            print("\nYou walked into the wall and put yourself in a coma. Tough luck.. Game Over!!")
    # Wrong choice made, game ends
    else:
        print("\nYou have been captured and sentenced to death by the king. Should have just asked for entry! Game Over!!")
# Wrong choice made, game ends
else:
    print("\nYou wandered into a forest and found yourself ripped apart by creatures in the shadows. Rough start? Game Over!!")