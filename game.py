import ctsp
import random_player
import adaptive_player
import random

TRIALS = 10000

class Game():

    def __init__(self, N, P1, P2, max_cost, max_benefit):

        self.game = ctsp.CTSP(N, max_cost, max_benefit)
        P1_home = random.randint(0, N - 1)
        P2_home = random.randint(0, N - 1)
        #print "Player 1 Home: " + str(P1_home)
        #print "Player 2 Home: " + str(P2_home)

        if P1 == 5:
            self.Player_1 = adaptive_player.Adaptive_Player(P1_home, self.game)
        else:
            self.Player_1 = random_player.Random_Player(P1, P1_home)

        if P2 == 5:
            self.Player_2 = adaptive_player.Adaptive_Player(P2_home, self.game)
        else:
            self.Player_2 = random_player.Random_Player(P2, P2_home)

    def game_result(self):

        #print("====================================\n"
        #      "              GAME OVER             \n"
        #      "====================================\n")

        #print "\n Results \n"

        #if self.Player_1.payoff > self.Player_2.payoff:
        #    print "\n PLAYER 1 WINS! \n"
        #    print "\n Player 1: " + str(self.Player_1.payoff)
        #    print "\n Player 2: " + str(self.Player_2.payoff)
        #    print "\n Player 1 traveled to " + str(len(self.Player_1.moves)) + " cities"
        #    print "\n Player 2 traveled to " + str(len(self.Player_2.moves)) + " cities"
        #else:
        #    print "\n PLAYER 2 WINS! \n"
        #    print "\n Player 1: " + str(self.Player_1.payoff)
        #    print "\n Player 2: " + str(self.Player_2.payoff)
        #    print "\n Player 1 traveled to " + str(len(self.Player_1.moves)) + " cities"
        #    print "\n Player 2 traveled to " + str(len(self.Player_2.moves)) + " cities"

        #print("====================================\n"
        #      "                TOURS               \n"
        #      "====================================\n")
        #print "Player 1 Tour: " + str(self.Player_1.moves)
        #print "Player 2 Tour: " + str(self.Player_2.moves)

        payoffs = [0, 0, 0, 0]
        payoffs[0] = self.Player_1.payoff
        payoffs[1] = self.Player_2.payoff
        payoffs[2] = len(self.Player_1.moves)
        payoffs[3] = len(self.Player_2.moves)
        return payoffs

def play(N, P1, P2, max_cost, max_benefit):

    #print("====================================\n"
    #      "     WELCOME TO THE CTSP GAME\n"
    #      "====================================\n")

    #print("Choose your fighter:\n\n"
    #      "1: Random Parametrized Heuristic Search\n"
    #      "2: Adaptive Search\n")

    #P = input("Selection: ")

    #if (P == 1):
    #    print("You selected Random. Please enter a probability between 0 and 1.\n")
    #    P1 = input("p = ")
    #    print "\n you selected probability p = " + str(P1) + "\n"
    #else:
    #    print "Not yet implemented..."
    #    exit(1)

    #print("\n====================================\n")


    #print("Choose your opponent:\n\n"
    #      "1: Simple Heuristic Search\n"
    #      "2: Adaptive Search\n")

    #Q = input("Selection: ")

    # if (Q == 1):
    #    print("You selected Random. Please enter a probability between 0 and 1.\n")
    #    P2 = input("p = ")
    #    print "\n you selected probability p = " + str(P2) + "\n"
    #else:
    #    print "Not yet implemented..."
    #    exit(1)

    # print "\n====================================\n"

    # N = input("Select a difficulty (Between 0 and 100) = ")

    # print "\n====================================\n"

    #max_cost = input("Maximum cost for this game is (between 1 and 100) = ")

    # print "\n====================================\n"

    #max_benefit = input("Maximum benefit for this game is (between 100 and 200 = ")

    # print "\n====================================\n"

    # print "            Initializing...           \n"

    game = Game(N, P1, P2, max_cost, max_benefit)

    city = game.game
    Player_1 = game.Player_1
    Player_2 = game.Player_2

    # print "\n====================================\n"

    # print "              FIGHT!                  \n"

    # print "======================================\n"


    # Play the game...
    T = 0
    while (True):

        # Time step
        T = T + 1

        #print "Time: " + str(T)
        #print "Player 1 Position: " + str(Player_1.position)
        #print "Player 2 Position: " + str(Player_2.position)

        #print "Unvisited cities: " + str(city.unvisited)

        # Are there no unvisited cities left?
        if (city.game_over()):
            break

        # Do we need to split the benefit for a city?
        if Player_1.can_move() and Player_2.can_move() and (Player_1.position == Player_2.position) and (T != 1):
            if Player_1.position in city.unvisited:
                Player_1.payoff += (city.benefits[Player_1.position] / 2)
                Player_2.payoff += (city.benefits[Player_2.position] / 2)
                city.unvisited.remove(Player_1.position)

                # Have Player 1 submit their proposed move
                P1_move = Player_1.move(city)
                Player_1.payoff -= city.cost_matrix[Player_1.position][P1_move]
                Player_1.position = P1_move

                # Have Player 2 submit their proposed move
                P2_move = Player_2.move(city)
                Player_2.payoff -= city.cost_matrix[Player_2.position][P2_move]
                Player_2.position = P2_move
        else:
            # Have Player 1 submit their proposed move
            if Player_1.can_move():
                if T != 1 and (Player_1.position in city.unvisited):
                    Player_1.payoff += city.benefits[Player_1.position]
                    city.unvisited.remove(Player_1.position)

                P1_move = Player_1.move(city)
                Player_1.payoff -= city.cost_matrix[Player_1.position][P1_move]

                Player_1.position = P1_move

            # Have Player 2 submit their proposed move
            if Player_2.can_move():
                if T != 1 and (Player_2.position in city.unvisited):
                    Player_2.payoff += city.benefits[Player_2.position]
                    city.unvisited.remove(Player_2.position)

                P2_move = Player_2.move(city)
                Player_2.payoff -= city.cost_matrix[Player_2.position][P2_move]

                Player_2.position = P2_move


        # Check if any services need to be paid for.
        # Players can only collect once they've waited time T = cost
        # Don't award anything for the first move
        #print "Player 1 Time: " + str(Player_1.time)
        #print "Player 2 Time: " + str(Player_2.time)

        if Player_1.time < Player_2.time:
            Player_2.time -= Player_1.time
            Player_1.time = 0
            assert (Player_1.time >= 0)
            assert (Player_2.time >= 0)
        elif Player_1.time > Player_2.time:
            Player_1.time -= Player_2.time
            Player_2.time = 0
            assert (Player_1.time >= 0)
            assert (Player_2.time >= 0)
        else:
            Player_1.time = 0
            Player_2.time = 0
            assert (Player_1.time >= 0)
            assert (Player_2.time >= 0)

    return game.game_result()

# Testing and Debugging
if __name__=="__main__":
    TRIALS = 1000
    Player1_payoff = 0
    Player2_payoff = 0
    Player1_moves = 0
    Player2_moves = 0

    for i in range(0, TRIALS):
        payoffs = play(50, 5, 1, 100, 1000)
        Player1_payoff += payoffs[0]
        Player2_payoff += payoffs[1]
        Player1_moves += payoffs[2]
        Player2_moves += payoffs[3]

    print "Average Payoffs\n"
    print "Player 1: " + str(float(Player1_payoff)/TRIALS)
    print "Player 2: " + str(float(Player2_payoff)/TRIALS)
    print "\nAverage Number of Moves\n"
    print "Player 1: " + str(float(Player1_moves)/TRIALS)
    print "Player 2: " + str(float(Player2_moves)/TRIALS)