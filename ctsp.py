import random
import numpy

def random_weighted_graph(N, max_cost):
    matrix = [[random.randint(1, max_cost) for i in range(N)] for j in range(N)]
    for i in range(N):
        matrix[i][i] = 0

    # If i is connected to j, j is connected to i
    for i in range(N):
        for j in range(N):
            matrix[j][i] = matrix[i][j]

    return matrix

class CTSP():

    def __init__(self, N, max_cost, max_benefit):

        self.cost_matrix = random_weighted_graph(N, max_cost)
        self.benefits = []
        self.unvisited = set()

        # The set of unvisited nodes is initially all of them
        for i in range(N):
            self.benefits.append(random.randint(max_cost, max_benefit))
            self.unvisited.add(i)

    def game_over(self):
        return len(self.unvisited) == 0

    # For the MCTS
    def get_legal_moves(self):
        return 0

    # For the MCTS
    def is_move_legal(self, move):
        return 0

if __name__=="__main__":

    game = CTSP(10, 100, 1000)
    print game.unvisited
    print game.benefits
    print numpy.matrix(game.cost_matrix)
    print game.game_over()
