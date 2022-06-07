import pickle
import time

from src.algorithm import *
from src.model import Board, Player, State, Config
from src.constant import ShapeConstant, GameConstant, Path
from src.utility import is_out, is_win, is_full, place

import sys

class Game:
    """
    Class represetation for Main Game

    [ATTRIBUTES]
        config: Config -> configuration used for gameplay
        state: State -> current state in a round
        bot: List[Bot] -> bot used in pvb or bvb

    [METHODS]
        __gen_player -> Generate player, if is_dump == True, 
            it will take bot from bin folder based on game type in config 
        __input -> Input for player
        __is_valid -> Check if input is valid
        __placement -> Placement phase for player or bot
    """
    def __init__(self, config: Config):
        self.config = config
        self.verbose = (self.config.game_type == GameConstant.BVB and self.config.verbose) or self.config.game_type != GameConstant.BVB
        if self.verbose:
            print(config)

        board = Board(config.row, config.col)
        players = [
            Player(GameConstant.PLAYER1_COLOR),
            Player(GameConstant.PLAYER2_COLOR),
        ]

        self.__gen_player()
        self.state = State(board, players, 1)

    def __gen_player(self):
        if self.config.game_type == GameConstant.BVB:
            if not self.config.is_dump:
                # Change this into your bots
                model1 = Bot13520101()
                model2 = Bot13520101()
            else:
                # Don't change this
                model1 = pickle.load(open(Path.BVB_P1, "rb"))
                model2 = pickle.load(open(Path.BVB_P2, "rb"))

            self.bot = [model1, model2]

        elif self.config.game_type == GameConstant.PVB:
            if not self.config.is_dump:
                # Change this into your bots
                model = Bot13520101()
            else:
                # Don't change this
                model = pickle.load(open(Path.PVB, "rb"))

            if self.config.player_choice == 0:
                self.bot = [None, model]
            else:
                self.bot = [model, None]
        else:
            self.bot = []

    def __input(self):
        choosen_col = int(input("Put Column: "))
        return choosen_col

    def __is_valid(self, choosen_col):
        # Check choosen_col is integer and in range
        if not isinstance(choosen_col, int):
            return False
        
        if not is_out(self.state.board, 0, choosen_col):
            return True

        return False

    def __placement(self, player):
        player_turn = (self.state.round - 1) % 2

        while True:
            if self.config.game_type == GameConstant.PVB:
                if player_turn == self.config.player_choice:
                    choosen_col = self.__input()
                else:
                    start = time.time()
                    choosen_col = self.bot[player_turn].find(
                        self.state, player_turn, self.config.thinking_time
                    )
                    if self.verbose:
                        print(f'Runtime: {time.time() - start}')

            elif self.config.game_type == GameConstant.PVP:
                choosen_col = self.__input()

            else:  # BVB
                start = time.time()
                choosen_col = self.bot[player_turn].find(
                    self.state, player_turn, self.config.thinking_time
                )
                if self.verbose:
                    print(f'Runtime: {time.time() - start}')

            
            if self.__is_valid(choosen_col):
                break

            if self.verbose:
                print(f"{choosen_col}  input are not valid")

        placement = place(self.state, player, choosen_col)
        return placement

    def gameplay(self):
        while True:
            player = (self.state.round - 1) % 2

            if self.verbose:
                print(f"Round {self.state.round}")
                print(self.state.board)
            placement = self.__placement(player)

            while placement == -1:
                if self.verbose:
                    print(self.state.board)
                placement = self.__placement(player)

            self.state.round += 1
            winner = is_win(self.state.board)
            if winner:
                if self.verbose:
                    print(self.state.board)
                break
            if is_full(self.state.board):
                break

        if winner:
            for i, player in enumerate(self.state.players):
                if winner == player.color:
                    if self.verbose:
                        print(
                            f"Player {i + 1} with color {player.color} Win"
                        )
                    return i
        else:
            if self.verbose:
                print("DRAW")
            return 2
