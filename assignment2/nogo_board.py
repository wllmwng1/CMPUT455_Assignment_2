"""
simple_board.py

Implements a basic Go board with functions to:
- initialize to a given board size
- check if a move is legal
- play a move

The board uses a 1-dimensional representation with padding
"""

import numpy as np
from board_util import GoBoardUtil, BLACK, WHITE, EMPTY, BORDER, \
                       PASS, is_black_white, coord_to_point, where1d, \
                       MAXSIZE, NULLPOINT

class NoGoBoard(object):

    def get_color(self, point):
        return self.board[point]

    def pt(self, row, col):
        return coord_to_point(row, col, self.size)

    def is_legal(self, point, color):
        """
        Check whether it is legal for color to play on point
        """
        board_copy = self.copy()
        # Try to play the move on a temporary copy of board
        # This prevents the board from being messed up by the move
        try:
            legal = board_copy.play_move(point, color)
        except ValueError:
            return False

        return legal

    def get_legal_moves(self, color):
        """
        Get the list of legal moves for the player toPlay
        """
        return GoBoardUtil.generate_legal_moves(self, color);


    def is_game_ended(self):
        """
        Check if the game has ended or not
        """
        current_player = self.current_player

        move = GoBoardUtil.generate_random_move(self, current_player, False)

        is_ended = not self.is_legal(move, current_player)

        return is_ended

    def _detect_captures(self, point, opp_color):
        """
        Did move on point capture something?
        """
        for nb in self.neighbors_of_color(point, opp_color):
            if self._detect_capture(nb):
                return True
        return False

    def get_empty_points(self):
        """
        Return:
            The empty points on the board
        """
        return where1d(self.board == EMPTY)

    def __init__(self, size):
        """
        Creates a Go board of given size
        """
        assert 2 <= size <= MAXSIZE
        self.reset(size)

    def reset(self, size):
        """
        Creates a start state, an empty board with the given size
        The board is stored as a one-dimensional array
        See GoBoardUtil.coord_to_point for explanations of the array encoding
        """
        self.size = size
        self.NS = size + 1
        self.WE = 1
        self.ko_recapture = None
        self.current_player = BLACK
        self.maxpoint = size * size + 3 * (size + 1)
        self.board = np.full(self.maxpoint, BORDER, dtype = np.int32)
        self.liberty_of = np.full(self.maxpoint, NULLPOINT, dtype = np.int32)
        self.moves = []
        self._initialize_empty_points(self.board)
        self._initialize_neighbors()

    def copy(self):
        b = NoGoBoard(self.size)
        assert b.NS == self.NS
        assert b.WE == self.WE
        b.ko_recapture = self.ko_recapture
        b.current_player = self.current_player
        assert b.maxpoint == self.maxpoint
        b.board = np.copy(self.board)
        return b

    def apply(self, new_board):
        assert new_board.size == self.size
        self.NS = new_board.NS
        self.WE = new_board.WE
        self.ko_recapture = new_board.ko_recapture
        self.current_player = new_board.current_player
        self.maxpoint = new_board.maxpoint
        self.board = np.copy(new_board.board)
        return

    def row_start(self, row):
        assert row >= 1
        assert row <= self.size
        return row * self.NS + 1

    def _initialize_empty_points(self, board):
        """
        Fills points on the board with EMPTY
        Argument
        ---------
        board: numpy array, filled with BORDER
        """
        for row in range(1, self.size + 1):
            start = self.row_start(row)
            board[start : start + self.size] = EMPTY

    def _on_board_neighbors(self, point):
        nbs = []
        for nb in self._neighbors(point):
            if self.board[nb] != BORDER:
                nbs.append(nb)
        return nbs

    def _initialize_neighbors(self):
        """
        precompute neighbor array.
        For each point on the board, store its list of on-the-board neighbors
        """
        self.neighbors = []
        for point in range(self.maxpoint):
            if self.board[point] == BORDER:
                self.neighbors.append([])
            else:
                self.neighbors.append(self._on_board_neighbors(point))

    def is_eye(self, point, color):
        """
        Check if point is a simple eye for color
        """
        if not self._is_surrounded(point, color):
            return False
        # Eye-like shape. Check diagonals to detect false eye
        opp_color = GoBoardUtil.opponent(color)
        false_count = 0
        at_edge = 0
        for d in self._diag_neighbors(point):
            if self.board[d] == BORDER:
                at_edge = 1
            elif self.board[d] == opp_color:
                false_count += 1
        return false_count <= 1 - at_edge # 0 at edge, 1 in center

    def _is_surrounded(self, point, color):
        """
        check whether empty point is surrounded by stones of color.
        """
        for nb in self.neighbors[point]:
            nb_color = self.board[nb]
            if nb_color != color:
                return False
        return True

    def _stone_has_liberty(self, stone):
        lib = self.find_neighbor_of_color(stone, EMPTY)
        return lib != None

    def _get_liberty(self, block):
        """
        Find any liberty of the given block.
        Returns None in case there is no liberty.
        block is a numpy boolean array
        """
        for stone in where1d(block):
            lib = self.find_neighbor_of_color(stone, EMPTY)
            if lib != None:
                return lib
        return None

    def _has_liberty(self, block):
        """
        Check if the given block has any liberty.
        Also updates the liberty_of array.
        block is a numpy boolean array
        """
        lib = self._get_liberty(block)
        if lib != None:
            assert self.get_color(lib) == EMPTY
            for stone in where1d(block):
                self.liberty_of[stone] = lib
            return True
        return False

    def _block_of(self, stone):
        """
        Find the block of given stone
        Returns a board of boolean markers which are set for
        all the points in the block
        """
        marker = np.full(self.maxpoint, False, dtype = bool)
        pointstack = [stone]
        color = self.get_color(stone)
        assert is_black_white(color)
        marker[stone] = True
        while pointstack:
            p = pointstack.pop()
            neighbors = self.neighbors_of_color(p, color)
            for nb in neighbors:
                if not marker[nb]:
                    marker[nb] = True
                    pointstack.append(nb)
        return marker

    def _fast_liberty_check(self, nb_point):
        lib = self.liberty_of[nb_point]
        if lib != NULLPOINT and self.get_color(lib) == EMPTY:
            return True # quick exit, block has a liberty
        if self._stone_has_liberty(nb_point):
            return True # quick exit, no need to look at whole block
        return False

    def _detect_capture(self, nb_point):
        """
        Check whether opponent block on nb_point is captured.
        Returns boolean.
        """
        if self._fast_liberty_check(nb_point):
            return False
        opp_block = self._block_of(nb_point)
        return not self._has_liberty(opp_block)

    def _detect_and_process_capture(self, nb_point):
        """
        Check whether opponent block on nb_point is captured.
        If yes, remove the stones.
        Returns the stone if only a single stone was captured,
            and returns None otherwise.
        This result is used in play_move to check for possible ko
        """
        opp_block = self._block_of(nb_point)
        if not self._has_liberty(opp_block):
            return True
        return False

    def play_move(self, point, color):
        """
        Play a move of color on point
        Returns boolean: whether move was legal
        """
        assert is_black_white(color)
        # Special cases
        if point == PASS:
            return False
        elif self.board[point] != EMPTY:
            raise ValueError("occupied")
        if point == self.ko_recapture:
            return False

        # General case: deal with captures, suicide, and next ko point
        opp_color = GoBoardUtil.opponent(color)
        in_enemy_eye = self._is_surrounded(point, opp_color)
        self.board[point] = color
        single_captures = []
        neighbors = self.neighbors[point]
        for nb in neighbors:
            if self.board[nb] == opp_color:
                single_capture = self._detect_and_process_capture(nb)
                if single_capture == True:
                    raise ValueError("capture")
        if not self._stone_has_liberty(point):
            # check suicide of whole block
            block = self._block_of(point)
            if not self._has_liberty(block): # undo suicide move
                self.board[point] = EMPTY
                raise ValueError("suicide")
        self.ko_recapture = None
        if in_enemy_eye and len(single_captures) == 1:
            self.ko_recapture = single_captures[0]
        self.moves.append([point,self.current_player])
        self.current_player = GoBoardUtil.opponent(color)
        return True

    def quicker_legal(self, point):

        color = self.current_player

        if point == PASS:
            return False
        elif self.board[point] != EMPTY:
            return False
        if point == self.ko_recapture:
            return False

        # General case: deal with captures, suicide, and next ko point
        opp_color = GoBoardUtil.opponent(color)
        in_enemy_eye = self._is_surrounded(point, opp_color)

        if in_enemy_eye:
            return False

        single_captures = []

        self.board[point] = color

        neighbors = self.neighbors[point]

        for nb in neighbors:
            if self.board[nb] == opp_color:
                if self._detect_capture(nb):
                    self.board[point] = EMPTY
                    return False

        if not self._stone_has_liberty(point):
            # check suicide of whole block
            block = self._block_of(point)
            if not self._has_liberty(block): # undo suicide move
                self.board[point] = EMPTY
                return False

        self.board[point] = EMPTY
        return True

    def blind_play(self, point, color):
        self.board[point] = color
        self.moves.append([point, self.current_player])
        self.current_player = GoBoardUtil.opponent(color)

    def undo_move(self):
        data = self.moves.pop()
        self.board[data[0]] = EMPTY
        self.current_player = data[1]

    def neighbors_of_color(self, point, color):
        """ List of neighbors of point of given color """
        nbc = []
        for nb in self.neighbors[point]:
            if self.get_color(nb) == color:
                nbc.append(nb)
        return nbc

    def find_neighbor_of_color(self, point, color):
        """ Return one neighbor of point of given color, or None """
        for nb in self.neighbors[point]:
            if self.get_color(nb) == color:
                return nb
        return None

    def _neighbors(self, point):
        """ List of all four neighbors of the point """
        return [point - 1, point + 1, point - self.NS, point + self.NS]

    def _diag_neighbors(self, point):
        """ List of all four diagonal neighbors of point """
        return [point - self.NS - 1,
                point - self.NS + 1,
                point + self.NS - 1,
                point + self.NS + 1]

    def _point_to_coord(self, point):
        """
        Transform point index to row, col.

        Arguments
        ---------
        point

        Returns
        -------
        x , y : int
        coordination of the board  1<= x <=size, 1<= y <=size .
        """
        if point is None:
            return 'pass'
        row, col = divmod(point, self.NS)
        return row, col

    def statisticallyEvaluateForToPlay(self):
        """
        Evaluates wins based on current_player.

        Arguments
        ---------
        None

        Returns
        -------
        win : boolean
        Whether or not the current player won.
        """

        cur_legal_moves = self.get_legal_moves(self.current_player)
        opp_legal_moves = self.get_legal_moves(GoBoardUtil.opponent(self.current_player))

        if len(cur_legal_moves) == 0:
            return False

        if len(opp_legal_moves) == 0:
            return True

        return None

    def code(self,tt):
        c = 0
        for x in range(self.size):
            for y in range(self.size):
                point = coord_to_point(x+1,y+1,self.size)
                c = c ^ tt.code[x*self.size+y][self.board[point]]
        return c

    def updateCode(self,tt,c,x,y,color):
        return c ^ tt.code[x-1*self.size+y-1][self.board[coord_to_point(x,y,self.size)]] ^ tt.code[x-1*self.size+y-1][color]

    def display(self):
        """
        displays the current Go board state
        """
        print(GoBoardUtil.get_twoD_board(self))
        return

    # def is_legal_gomoku(self, point, color):
    #     """
    #         Check whether it is legal for color to play on point, for the game of gomoku
    #         """
    #     return self.board[point] == EMPTY

    # def play_move_gomoku(self, point, color):
    #     """
    #         Play a move of color on point, for the game of gomoku
    #         Returns boolean: whether move was legal
    #         """
    #     assert is_black_white(color)
    #     assert point != PASS
    #     if self.board[point] != EMPTY:
    #         return False
    #     self.board[point] = color
    #     self.current_player = GoBoardUtil.opponent(color)
    #     return True

    # def _point_direction_check_connect_gomoko(self, point, shift):
    #     """
    #     Check if the point has connect5 condition in a direction
    #     for the game of Gomoko.
    #     """
    #     color = self.board[point]
    #     count = 1
    #     d = shift
    #     p = point
    #     while True:
    #         p = p + d
    #         if self.board[p] == color:
    #             count = count + 1
    #             if count == 5:
    #                 break
    #         else:
    #             break
    #     d = -d
    #     p = point
    #     while True:
    #         p = p + d
    #         if self.board[p] == color:
    #             count = count + 1
    #             if count == 5:
    #                 break
    #         else:
    #             break
    #     assert count <= 5
    #     return count == 5

    # def point_check_game_end_gomoku(self, point):
    #     """
    #         Check if the point causes the game end for the game of Gomoko.
    #         """
    #     # check horizontal
    #     if self._point_direction_check_connect_gomoko(point, 1):
    #         return True

    #     # check vertical
    #     if self._point_direction_check_connect_gomoko(point, self.NS):
    #         return True

    #     # check y=x
    #     if self._point_direction_check_connect_gomoko(point, self.NS + 1):
    #         return True

    #     # check y=-x
    #     if self._point_direction_check_connect_gomoko(point, self.NS - 1):
    #         return True

    #     return False

    # def check_game_end_gomoku(self):
    #     """
    #         Check if the game ends for the game of Gomoku.
    #         """
    #     white_points = where1d(self.board == WHITE)
    #     black_points = where1d(self.board == BLACK)

    #     for point in white_points:
    #         if self.point_check_game_end_gomoku(point):
    #             return True, WHITE

    #     for point in black_points:
    #         if self.point_check_game_end_gomoku(point):
    #             return True, BLACK

    #     return False, None
