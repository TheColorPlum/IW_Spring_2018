import numpy.random as random

W = .90

class Adaptive_Player():

    def __init__(self, home, game):

        # Player State Components
        self.home = home
        self.position = home
        self.payoff = 0
        self.time = 0
        self.moves = set()

        # Opponent State Components
        self.opponent_home = -1  # Where we think our opponent started
        self.opponent_position = -1  # Where we think our opponent is
        self.opponent_payoff = 0
        self.opponent_moves = set()

        # Game State Components
        self.opponent_guesses = [-1, -1, -1]
        self.guesses_correct = [False, False, False] # Did the guesses match the next move?
        self.strategy_probabilities = [.33, .33, .34] # Probability that the opponent plays a given strategy
        self.V = set() # Set of all nodes in the graph
        for i in range(len(game.benefits)):
            self.V.add(i)

    def expected_payoff(self, game):

        expected_payoff_aggressive = 0
        expected_payoff_adjusted_hp = 0

        i = 0
        for guess in self.opponent_guesses:

            # First see if I can beat them there
            their_time = game.cost_matrix[self.opponent_position][guess]
            my_time = game.cost_matrix[self.position][guess]

            if their_time < my_time:
                expected_payoff_aggressive += 0
            else:
                expected_payoff_aggressive += self.strategy_probabilities[i] * (game.benefits[guess] - my_time)

            # Compute expected payoff of adjusted hp
            adjusted = set()
            adjusted.add(guess)
            adjusted = set.copy(game.unvisited) - adjusted

            # Highest Payoff Strategy
            distances = game.cost_matrix[self.home]
            max = -float('inf')
            move = 0
            for neighbor in adjusted:
                payoff = game.benefits[neighbor] - distances[neighbor]
                if max < payoff and (neighbor != self.position):
                    move = neighbor

            expected_payoff_adjusted_hp += self.strategy_probabilities[i] * (game.benefits[move] - distances[move])

            i += 1


        return (expected_payoff_aggressive >= expected_payoff_adjusted_hp)

    def simulate_nun(self, position, game):

        # Nearest Unvisited Neighbor Strategy
        distances = game.cost_matrix[self.home]
        min = float('inf')
        move = list(game.unvisited)[0]

        if len(game.unvisited) == 1:
            return move

        for neighbor in game.unvisited:
            if min > distances[neighbor] and (neighbor != position):
                move = neighbor

        return move

    def simulate_hb(self, position, game):

        # Highest Benefit Strategy
        max = -float('inf')
        move = list(game.unvisited)[0]

        if len(game.unvisited) == 1:
            return move

        for neighbor in game.unvisited:
            if max < game.benefits[neighbor] and (neighbor != position):
                move = neighbor

        return move

    def simulate_hp(self, position, game):

        # Highest Payoff Strategy
        distances = game.cost_matrix[self.home]
        max = -float('inf')
        move = list(game.unvisited)[0]

        if len(game.unvisited) == 1:
            return move

        for neighbor in game.unvisited:
            payoff = game.benefits[neighbor] - distances[neighbor]
            if max < payoff and (neighbor != position):
                move = neighbor

        return move

    def can_move(self):
        return (self.time == 0)

    def move(self, game):

        # Is the game over? If so, go home
        if game.game_over():
            return self.home

        unvisited = game.unvisited
        benefits = game.benefits
        cost_matrix = game.cost_matrix

        # Infer some information about your opponent from the game state
        # Find Y, the set of all visited nodes in the graph
        Z = self.V - unvisited
        Y = Z - self.moves

        # Now determine what my greedy move would be
        # Select the neighbor that will produce the most payoff
        greedy_move = -1
        max = -float('inf')
        for neighbor in unvisited:
            payoff = benefits[neighbor] - cost_matrix[self.position][neighbor]
            if max < payoff:
                greedy_move = neighbor

        # Have we seen a move by the opponent?
        X = Y - self.opponent_moves
        # If we haven't play greedily
        if len(Y) == 0:
            return greedy_move
        else:
            # If this is the first change we've seen in the set, select a home
            # Note: An assumption made here is that
            if self.opponent_home == -1:
                self.opponent_home = random.choice(list(Y))
                self.opponent_position = self.opponent_home
            else:
                # If there was a change, set the opponent's position to one of the newly visited nodes
                self.opponent_position = random.choice(list(X))

        # Were any of our guesses correct?
        correct = 0
        i = 0
        for move in self.opponent_guesses:
            if move in X:
                correct += 1
                self.guesses_correct[i] = True
            else:
                self.guesses_correct[i] = False
            i += 1

        # Redistribute strategy probabilities
        i = 0
        if correct > 0:
            for strategy in self.strategy_probabilities:
                strategy = W * strategy
                if self.guesses_correct[i]:
                    strategy += (1 - W)/correct
                i += 1

        # From the opponent position construct the game tree
        # Highest Benefit move?
        self.opponent_guesses[0] = self.simulate_hb(self.opponent_position, game)

        # Nearest Unvisited Neighbor move?
        self.opponent_guesses[1] = self.simulate_nun(self.opponent_position, game)

        # Highest Payoff move?
        self.opponent_guesses[2] = self.simulate_hp(self.opponent_position, game)

        # Should we play aggressively?
        aggressive = self.expected_payoff(game)

        if aggressive:
            #print self.opponent_guesses
            #print self.strategy_probabilities
            move = random.choice(self.opponent_guesses, p=self.strategy_probabilities)
            #print move
            self.moves.add(move)
            return move
        else:
            move = self.simulate_hp(self.position, game)
            self.moves.add(move)
            return move