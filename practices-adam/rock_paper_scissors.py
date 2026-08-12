from random import randint
count = 0
wins = 0
losses = 0
ties = 0
while count < 5:
    randomChoice = randint(1,3)

    if randomChoice == 1:
        randomChoice = "Rock"
    elif randomChoice == 2:
        randomChoice = "Paper"
    else:
        randomChoice = "Scissors"

    try: 
        playerChoice = int(input(" Welcome to Rock Paper Scissors! Please choose your weapon: 1 = Rock, 2 = Paper, 3 = Scissors: "))
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 3.")
        continue

    if playerChoice < 1 or playerChoice > 3:
        print("Invalid input. Please enter a number between 1 and 3.")
        continue

    if playerChoice == 1:
        playerChoice = "Rock"
    elif playerChoice == 2:
        playerChoice = "Paper"
    else:
        playerChoice = "Scissors"

    if playerChoice == randomChoice:
        ties += 1
        print("You chose ", playerChoice , "and the computer chose", randomChoice , "It's a tie!")
    elif playerChoice == "Paper" and randomChoice == "Rock":
        wins += 1
        print("You chose ", playerChoice , "and the computer chose", randomChoice , "You win!")
    elif playerChoice == "Rock" and randomChoice == "Scissors":
        wins += 1
        print("You chose ", playerChoice , "and the computer chose", randomChoice , "You win!")
    elif playerChoice == "Scissors" and randomChoice == "Paper":
        wins += 1
        print("You chose ", playerChoice , "and the computer chose", randomChoice , "You win!")
    else:
        losses += 1
        print("You chose ", playerChoice , "and the computer chose", randomChoice , "You lose!")

    count += 1


print("You have won", wins, "games, lost", losses, "games, and tied", ties, "games.")

if wins > losses:
    print("You won the game!")
elif wins < losses:
    print("You lost the game!")
else:
    print("The game is a tie!")