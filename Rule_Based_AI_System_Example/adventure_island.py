print("Welcome to Adventure Island!\n")
print("Your goal is to find the kings treasure hidden deep within the island.\n")
choice1 = input("You are at a fork in the road. Do you want to go left or right?\n"
                "Type 'left' or 'right': \n").lower()

if choice1 == "left":
    choice2 = input("\nYou've come to a castle. There is a hole within the wall to the left and the main gate to the right.\n"
                    "Do you want to go through the hole or approach the gate? (Type 'hole' or 'gate'): \n").lower()
    if choice2 == "gate":
        choice3 = input("\nYour are granted entry into the castle hall. There are 3 doors.\n"
                        "One Red, one Yellow, and One Blue. Which door do you choose?\n"
                        "Type 'red', 'yellow', 'blue', or any other color if you're feeling adventurous: \n").lower()
        if choice3 == "red":
            print("\nYou have entered a room full of demons. You simply cannot escape. Game Over!!")
        elif choice3 == "yellow":
            print("\nYou have found the castles dragon! It burns you to a crisp. Game Over!!")
        elif choice3 == "blue":
            print("\nYou have found the kings treasure and become the new ruler of the island! You win!!")
        else:
            print("\nYou walked into the wall and put yourself in a coma. Tough luck.. Game Over!!")
    else:
        print("\nYou have been captured and sentenced to death by the king. Should have just asked for entry! Game Over!!")
else:
    print("\nYou wandered into a forest and found yourself ripped apart by creatures in the shadows. Rough start? Game Over!!")