import random
import string

def rollDice(numDice):
    """
        This function returns the score a player gets in a round by rolling some dice.
        If there is one dice with 1, the score of this round is 1;
        otherwise, the score is the sum of all dice.
    """
    totalScore = 0
    for i in range(0, numDice):
        num = random.random()
        score = int(num * 6 + 1)
        totalScore += score
        #we know the score of the round is 1 as soon as we see one dice with 1
        if score == 1:
            return 1
    return totalScore
    
def takeTurn(opponentScore, numDice):
    """
        This function returns the score a player gets in a round given the score of his/her
        opponent and the number of dice he/she chooses to roll. 
    """
    tens = opponentScore // 10
    ones = opponentScore - tens * 10
    #if the player chooses to roll zero dice, he/she receives a score of one greater than
    #the greater of the digits of his/her opponent's score
    if numDice == 0: 
        return max(ones, tens) + 1
    #if the player chooses to roll non-zero dice, he/she receives a score of actually 
    #rolling dice
    else:
        return rollDice(numDice)
         
def roll3UnlessCloseToEnd(score, opponentScore, goalScore, remainingTurns = 0):
    """
        This function is a strategy for playing the game. The computer player always 
        rolls three dice except in two specific cases. If the opponent could win by 
        rolling a single six on the next turn and the computer score is less than 70% of 
        the goal score, then the computer rolls eight dice. If the computer score is 
        greater than 90% of the goal score, then the computer rolls two dice. The 
        function returns the number of dice that this player has chosen to roll. 
    """
    #If the opponent could win by rolling a single six on the next turn and the 
    #computer score is less than 70% of the goal score
    if (goalScore - opponentScore <= 6) and (score < 0.7 * goalScore):
        return 8
    #If the computer score is greater than 90% of the goal score
    elif score >= 0.9 * goalScore:
        return 2
    #default choice
    else: return 3

def humanPlayer(score, opponentScore, goalScore, remainingTurns = 0):
    """
        This function lets a human player actually play the game. The function tells the 
        human player of current scores and the goal score; then ask for the human player's
        choice. This function returns the number of dice the human player chose to roll.
    """
    print("Your score is", score, ", your opponent's score is", opponentScore, ", and the goal is", goalScore, ".")
    numberAsAString = input("Enter in the number of dice to roll (0-10):")
    numberAsAString = int(numberAsAString)
    print("You chose", numberAsAString, ".")
    return int(numberAsAString)
    
def playPig(goalScore, maxRounds, strategy1, strategy2):
    """
        This function simulates a game of pig. The game has a goal score of goalScore and 
        allows a maximum of maxRounds rounds. Player 1 deploys strategy1 while player 2 
        deploys strategy 2. This function returns 1 if player 1 wins, 0 if they tie, and
        -1 if player 2 wins.
    """
    player1Score = 0
    player2Score = 0
    for rounds in range(0, maxRounds):
        player1Score += takeTurn(player2Score, strategy1(player1Score, player2Score, goalScore, maxRounds - rounds))
        #decide if player 1 wins after rolling a dice by achieving goal score
        if player1Score >= goalScore: return 1
        player2Score += takeTurn(player1Score, strategy2(player2Score, player1Score, goalScore, maxRounds - rounds))
        #decide if player 2 wins after rolling a dice by achieving goal score
        if player2Score >= goalScore: return -1
    #decide the result after maximum number of rounds have been played
    if player1Score > player2Score: return 1
    if player1Score == player2Score: return 0
    if player1Score < player2Score: return -1
    
def main():
    """
        This is the main function. This function simulates an instance of the game. Goal
        score is set to be 100 and a maximun of 20 rounds is allowed. Player 1 is the 
        computer player deploying roll3UnlessCloseToEnd and player 2 is a human player.
        This function prints the result of the game.
    """
    outcome = playPig(100, 20, roll3UnlessCloseToEnd, humanPlayer)
    if outcome == 1: print("Player 1 wins!")
    if outcome == 0: print("Tie!")
    if outcome == -1: print("Player 2 wins!")
    
def averageScoreForDice(numDice, numSimulations):
    """ This function aims to determine the average score per turn, using between 
		0 and 10 dye.
		parameters: 
		numDice - the number of dye thrown each term, between 0 and 10
		numSimulations - the number of simulations run, throwing a specific number of dye
	"""
    testingScore = 0
    for i in range(numSimulations + 1):
        testingScore += rollDice(numDice)
    averageScore = testingScore / numSimulations
    return averageScore

def maximumAverageScoreAction(numSimulations):
    """	This function uses the function averageScoreForDice to determine which number of 
		dice gives the highest score by comparing the average score produced using
		different numbers of dye. 
		parameters: 
		numSimulations - the number of simulations run, throwing a specific number of dye
	"""
    bestNum = 0
    bestScore = -9999
    for num in range(1, 11):
        score = averageScoreForDice(num, numSimulations)
        if score >= bestScore:
            bestNum = num
            bestScore = score
    return bestNum

def runExperiment(numSimulations, strategy):
    """ This function compares a specific strategies with computer's strategy using a 
        given number of simulations, and the goal score is 100 with 20 round maximun in 
        each simulation. It will give the winning rate of the specific strategy.
	"""
    player1Round = 0
    for i in range(numSimulations + 1):
        outcome = playPig(100, 20, strategy, roll3UnlessCloseToEnd)
        if outcome == 1: player1Round += 1
    percentage = (player1Round / numSimulations) * 100
    print(str(percentage) + "%")
 
            
def bestStrategy(score, opponentScore, goalScore):
    """ Our best strategy is to go 0 or otherwise 6. Our default is to roll
        six dice but we adjust this based on the opponent score and previous rolls.  
	"""
    tens = opponentScore // 10
    ones = opponentScore - tens * 10
    #If we can guarantee to win by roll 0 dice, the strategy goes zero dice.
    if (goalScore - score) <= max(ones, tens) + 1 : return 0
    #According to the function of averageScoreForDice we defined above, the best score is 
    #8.7 by 6 dice, so if we can reach that by rolling 0 dice, the strategy goes 0 dice.
    if max(ones, tens) + 1 > 8 : return 0
     #If the opponent is close enough to win the game and we are still far from the goal,
    #it would be better to take a risk by rolling 8 dice.
    if (goalScore - opponentScore <= 6) and (score < 0.7 * goalScore): return 8
   #Other than that, roll 6 dice.
    return 6
    



        
if __name__ == "__main__":
        main()
