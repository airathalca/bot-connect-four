import copy
import math
import time
from src.constant import ColorConstant, GameConstant, ShapeConstant
from src.model import State, Piece
from src.utility import is_out

class Bot13520101:
    def __init__(self) -> None:
        pass
    def find(self, state: State, player: int, thinking_time: float) -> int:
        """
        [DESC]
            Function to find the best move for player
        [PARAMS]
            state: State -> current state
            player: int -> player to find the best move
            thinking_time: float -> time limit for bot to find the best move
        [RETURN]
            int -> column to place piece
        """
        prio_col = [i for i in range(state.board.col)]
        low_row = [-1 for i in range(state.board.col)]
        value = [-math.inf for i in range(state.board.col)]
        prio_col = sorted_from_middle(prio_col)
        for i in range (state.board.col):
            for j in range (state.board.row - 1, -1, -1):
                if state.board.__getitem__([j,i]).shape == ShapeConstant.BLANK:
                    low_row[i] = j
                    break
        for i in range (state.board.col):
            if low_row[i] != -1:
                value[i] = self.heuristic(state, player, low_row[i], i)
        indices = [i for i, x in enumerate(value) if x == max(value)]
        for i in range (len(prio_col)):
            if prio_col[i] in indices:
                return prio_col[i]
    
    def heuristic(self, state: State, player: int, low_row: int, col: int) -> int:
        value = 0
        piece = Piece(GameConstant.PLAYER_SHAPE, GameConstant.PLAYER_COLOR[player])
        state = copy.copy(state)
        state.board.set_piece(low_row, col, piece)
        for i in range(state.board.row):
            if state.board.__getitem__([i, state.board.col // 2]).color == GameConstant.PLAYER_COLOR[player]:
                value += 3
            for j in range(state.board.col):
                    value += self.check_streak(state, i, j, player)
        state.board.set_piece(low_row, col, Piece(ShapeConstant.BLANK, ColorConstant.BLACK))
        return value
    
    def check_streak(self, state: State, row: int, col: int, player: int) -> int:
        c_player = GameConstant.PLAYER_COLOR[player]
        c_enemy = GameConstant.PLAYER_COLOR[(player + 1) % 2]
        c_blank = ColorConstant.BLACK
        ans = 0
        row_ax = [1, 0, 1, -1]
        col_ax = [1, 1, 0, 1]
        for i in range(4):
            row_ = row + row_ax[i]*GameConstant.N_COMPONENT_STREAK - 1
            col_ = col + col_ax[i]*GameConstant.N_COMPONENT_STREAK - 1
            if is_out(state.board, row_, col_):
                continue
            else:
                check = [state.board.__getitem__([row + row_ax[i]*j, col + col_ax[i]*j]).color for j in range (GameConstant.N_COMPONENT_STREAK)]
                if (check.count(c_player) == GameConstant.N_COMPONENT_STREAK):
                    ans += 10000000000
                elif (check.count(c_player) == GameConstant.N_COMPONENT_STREAK - 1) and (check.count(c_blank) == 1):
                    ans += 5
                elif (check.count(c_player) == GameConstant.N_COMPONENT_STREAK - 2) and (check.count(c_blank) == 2):
                    ans += 2
                elif (check.count(c_enemy) == GameConstant.N_COMPONENT_STREAK - 2) and (check.count(c_blank) == 2):
                    ans -= 3
                elif (check.count(c_enemy) == GameConstant.N_COMPONENT_STREAK - 1):
                    if (check.count(c_blank) == 1):
                        idx_blank = check.index(c_blank)
                        if (row + row_ax[i]*idx_blank == state.board.row - 1):
                            ans -= 10000000000
                        elif (state.board.__getitem__([row + row_ax[i]*idx_blank + 1, col + col_ax[i]*idx_blank]).shape != ShapeConstant.BLANK):
                            ans -= 10000000000
                        else:
                            ans -= 5
        return ans

def sorted_from_middle(lst):
    left = lst[len(lst)//2-1::-1]
    right = lst[len(lst)//2:]
    output = [right.pop(0)] if len(lst) % 2 else []
    for t in zip(left, right):
        output += sorted(t, reverse=False)
    return output