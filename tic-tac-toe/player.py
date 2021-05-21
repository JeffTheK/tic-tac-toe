import math 
import random

class Player:
    def __init__(self, letter):
        # letter is x or o
        self.letter = letter

    # all players to get their next move given a game
    def get_move():
        pass

class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        # get a random valid spot for our next move
        square = random.choice(game.available_moves())
        return square

class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + '\'s turn. Input move (0-8):')
            # going to check that this is a correct value by trying to cast
            # it to an integer, and if it's not, then say its invalid
            # if that spot is not available on the board, also say its invalid
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True 
            except ValueError:
                print('Invalid square. Try again.')

        return val

class SmartComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            square = random.choice(game.avalaible_moves()) # randomly choose me
        else:
            #get the square based off the minimax algorithm
            square = self.minimax(game, self.letter)['position']
        return square

    def minimax(self, state, player):
        max_player = self.letter # yourself 
        other_player = 'O' if player == 'X' else 'X' # the other player... so whatever letter is NO

        # first, we want to check if the previous move is a winner
        # this is our base case
        if state.current_winner == other_player:
            return {'position': None,
                'score' : 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (state.num_empty_squares() +1)
                }

        elif not state.empty_squares(): # no empty squares
            return {'position': None, 'score': 0}

        #initalize some doctionaries
        if player == max_player:
            best = {'position': None, 'score': -math.inf} # each score should maximize (be larger)
        else:
            best = {'position': None, 'score': math.inf}

        for possible_move in state.available_moves():
            # 1: make a move, try that spot
            state.make_move(possible_move, player)
            # 2: recurse using minimax to simulate a game after making that move
            sim_score = self.minimax(state, other_player) # alternate players

            # 3: undo the move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move # otherwise this will get messed up from the recursiion

            # 4: update the dictionaries if necessary
            if player == max_player: # we are trying to maximize the max_player
                if sim_score['score'] > best['score']:
                    best = sim_score # replace best
            else: # but minimize the other player
                if sim_score['score'] < best['score']:
                    best = sim_score # 
        return best
