import random

class Random_Player():

    def __init__(self, P, home):

        self.P = P
        self.home = home
        self.position = home
        self.payoff = 0
        self.time = 0
        self.moves = set()
        self.strategies = set()

        # Pure or Mixed Strategy
        if P == 1:
            self.strategies.add(1)
        elif P == 2:
            self.strategies.add(2)
        elif P == 3:
            self.strategies.add(3)
        else:
            self.strategies.add(1)
            self.strategies.add(2)
            self.strategies.add(3)

    def can_move(self):
        return (self.time == 0)

    def move(self, game):

        # Is the game over? If so, go home
        if game.game_over():
            return self.home

        # Otherwise, decide what strategy I'm going to play
        unvisited = game.unvisited
        benefits = game.benefits
        cost_matrix = game.cost_matrix
        strategy = random.choice(list(self.strategies)) # Return a number in (0, 1)

        # Play the selected strategy
        if strategy == 1:

            # Highest Benefit Strategy
            max = -float('inf')
            move = list(unvisited)[0]

            if len(unvisited) == 1:
                return move

            for neighbor in unvisited:
                if max < benefits[neighbor] and (neighbor != self.position):
                    move = neighbor

            self.moves.add(move)
            self.time += cost_matrix[self.position][move]
            #print "My greedy move is: " + str(move)
            return move

        elif strategy == 2:

            # Nearest Unvisited Neighbor Strategy
            distances = cost_matrix[self.home]
            min = float('inf')
            move = list(unvisited)[0]

            if len(unvisited) == 1:
                return move

            for neighbor in unvisited:
                if min > distances[neighbor] and (neighbor != self.position):
                    move = neighbor

            self.moves.add(move)
            self.time += cost_matrix[self.position][move]
            #print "My nearest move is: " + str(move)
            return move

        else:
            # Highest Payoff Strategy
            distances = cost_matrix[self.home]
            max = -float('inf')
            move = list(unvisited)[0]

            if len(unvisited) == 1:
                return move

            for neighbor in unvisited:
                payoff = benefits[neighbor] - distances[neighbor]
                if max < payoff and (neighbor != self.position):
                    move = neighbor

            self.moves.add(move)
            self.time += cost_matrix[self.position][move]
            #print "My highest payoff move is: " + str(move)
            return move

# Testing and Debugging
if __name__=="__main__":

    strategies = [True, True, False]
    for i in strategies:
        print i