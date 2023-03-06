# Bobby Craft
# Date: 6-3-22
# Description: Intro to Comp Sci II: Module 10 Project


class GoBoard:
    
    def __init__(self) -> None:
        """
        Gess gameboard class. Initializes an empty 
        game board, black stone and white stones positions.
        """
        self._game_board = [[''] * 20 for _ in range(20)]
        
        self._black_stones = ['c2', 'e2', 'g2', 'h2', 'i2', 'j2', 'k2', 'l2', 
                              'm2', 'n2', 'p2', 'r2', 'b3', 'c3', 'd3', 'f3', 
                              'h3', 'i3', 'j3', 'k3', 'm3', 'o3', 'q3', 'r3', 
                              's3', 'c4', 'e4', 'g4', 'h4', 'i4', 'j4', 'k4', 
                              'l4', 'm4', 'n4', 'p4', 'r4', 'c7', 'f7', 'i7', 
                              'l7', 'o7', 'r7']

        self._white_stones = ['c19', 'e19', 'g19', 'h19', 'i19', 'j19', 'k19', 
                              'l19', 'm19', 'n19', 'p19', 'r19', 'b18', 'c18', 
                              'd18', 'f18', 'h18', 'i18', 'j18', 'k18', 'm18', 
                              'o18', 'q18', 'r18', 's18', 'c17', 'e17', 'g17', 
                              'h17', 'i17', 'j17', 'k17', 'l17', 'm17', 'n17', 
                              'p17', 'r17', 'c14', 'f14', 'i14', 'l14', 'o14', 
                              'r14']
                              

class GessGame:
    """
    Includes methods for starting a new game; 
    making moves; tracking game state; resigning players
    """
    
    def __init__(self):
        """
        Creates new Gess game object; Initializes empty game 
        board object; game piece; current game state to 'UNFINISHED'; 
        and starting player to 'BLK'.
        """
        self._ftprint = [[''] * 3 for _ in range(3)]  # 3x3 game piece
        self._alpha_to = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 
                          'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 
                          'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16, 
                          'r': 17, 's': 18, 't': 19}  # position from str to int
        self._board = []
        self._blk_rings_left = 1
        self._wht_rings_left = 1
        self._current_state = 'UNFINISHED'
        self._player_to_move = 'B'
        self._other_player = 'W'
        self._prev_move = None
        self._blk_stones_left = 43
        self._wht_stones_left = 43

    
    def set_game_board(self):
        """
        Sets up the Go board with stones assigned to their respective squares. 
        Returns the resulting board.
        """
        self._board = GoBoard()._game_board

        for stone, color in [(s, 'B') for s in GoBoard()._black_stones] + \
            [(s, 'W') for s in GoBoard()._white_stones]:
            col = self._alpha_to[stone[0].lower()]  # convert position to int
            row = int(stone[1:]) - 1
            self._board[row][col] = color  # assign stone color to square

        return self._board


    def get_game_board(self):
        """
        Returns current game board state 
        """
        return self._board


    def get_blk_ring_counter(self):
        """
        Returns num of remaining black rings 
        """
        return self._blk_rings_left
    
    
    def get_wht_ring_counter(self):
        """
        Returns num of remaining white rings 
        """
        return self._wht_rings_left


    def get_game_stone_count(self):
        """
        Remaining 'BLK' and 'WHT'stones 
        """
        print("Total black stones left:", self._blk_stones_left)
        print("Total white stones left:", self._wht_stones_left)
        return


    def get_ftprint(self):
        """Returns current game piece"""
        return self._ftprint


    def get_game_state(self):
        """Returns 'UNFINISHED', 'BLACK_WON' or 'WHITE_WON'"""
        return self._current_state


    def get_current_player(self):
        """Tracks current player - 'BLK' or 'WHT'"""
        return self._player_to_move


    def get_prev_move(self):
        """Tracks previous move - 'BLK' or 'WHT'"""
        return self._prev_move


    def set_ftprint(self, fr_row, fr_col):
        """
        Sets-up piece denoted by a 3x3 matrix with 
        [fr_row][fr_col] as center square. Returns
        game 3x3 footprint
        """
        board = self.get_game_board()
        offsets = [-1, 0, 1]
        for i in offsets:
            for j in offsets:
                self._ftprint[i+1][j+1] = board[fr_row+i][fr_col+j]

        return self._ftprint


    def update_fr_position(self, fr_row, fr_col, board):
        """
        Empties the origin squares covered by the 3x3 piece to prepare for the move.  
        """
        positions = [(fr_row+i, fr_col+j) for i in [-1, 0, 1] for j in [-1, 0, 1]]
        for i, j in positions:
            board[i][j] = ''


    def update_to_position(self, to_row, to_col, board, ftprint):
        """
        Updates the board destination squares after moving the 3x3 
        footprint. Captures any stones occupying the destination 
        squares.
        """
        for i in range(3):
            for j in range(3):
                board[to_row-1+i][to_col-1+j] = ftprint[i][j]


    def update_board(self,fr_row, fr_col, to_row, to_col):
        """
        Updates the game board after moving a piece. Removes any stones 
        overlapped by the 3x3 footprint of the piece, and stops movement 
        as soon as overlap occurs. 
        """

        self.update_fr_position(fr_row, fr_col, self._board)
        self.update_to_position(to_row, to_col, self._board, self.get_ftprint()) 
        return self._board


    def check_if_players_turn(self, fr_space, to_space):
        """
       Determine if the current player can legally make the given move. Returns 
       True if valid and current player's turn, else False.
        """
        if self.make_move(fr_space, to_space): # if move legal
            if self._player_to_move == self._prev_move:
                print("It's the other player's turn! >:-<")
                return False
            return True
        return False
    

    def is_piece_legal(self):
        """
        Check if a piece is legal by examining the 3x3 matrix centered on it. An 
        illegal piece contains the other player's stone or no stones belonging to 
        the current player.
        """

        if self.get_ftprint()[1][1] == self._other_player:
            return False

        # Check squares surrounding center
        for i, j in [(i, j) for i in range(3) for j in range(3) if (i, j) != (1, 1)]: 
            # Invalid: if other player's stone is found
            if self.get_ftprint()[i][j] == self._other_player:
                return False

            # Valid: if only current player's stone is found
            if self.get_ftprint()[i][j] == self._player_to_move:
                return True

        # Invalid: if no current player's stones are found
        return False
            

    def is_move_legal(self, fr_row, to_row, fr_col, to_col):
        """
        Check if a move from (fr_row, fr_col) to (to_row, to_col) is legal.
        Return True if the move is valid, False otherwise.
        """
        
        if not self.is_piece_legal() or (to_row, to_col) == (fr_row, fr_col):
            return False 

        # Check if destination square is out-of-bounds
        if not 1 <= to_row <= 18 or not 1 <= to_col <= 18:
            return False

        # Check if starting square is out-of-bounds
        if not 1 <= fr_row <= 18 or not 1 <= fr_col <= 18:
            return False

        return True


    def remove_captured_stones_vert(self, start_row, beg_row, end_row, fr_col):
        """
        Removes any overlapped stones (BLK or WHT)
        in path of piece movement (N or S)
        """

        board = self.get_game_board()
        stone_count = {'B': self._blk_stones_left, 'W': self._wht_stones_left}

        for row in range(beg_row, end_row):
            for col in range(fr_col-1, fr_col+2):
                stone = board[row][col]
                if stone in stone_count:
                    stone_count[stone] -= (row == start_row or row in (0, 19))
                    board[row][col] = ''

        return board


    def remove_captured_stones_horiz(self, start_col, row, beg_col, end_col):
        """
        Removes any overlapped stones (BLK or WHT)
        in path of piece movement (E or W)
        """
        board = self.get_game_board()
        stone_count = {'B': self._blk_stones_left, 'W': self._wht_stones_left}

        for r in range(row - 1, row + 2):
            for c in range(beg_col, end_col):
                if c in (0, 19):
                    stone = board[r][start_col]
                else:
                    stone = board[r][c]
                if stone in stone_count:
                    stone_count[stone] -= 1
                    board[r][c] = ''

        return board

    def determine_move_direction(self, fr_row, to_row, fr_col, to_col, row, col):
        """
        Returns diagonal direction piece will move
        """
        dir, out = None, None
        if fr_row > to_row:
            dir = self.move_nw if fr_col > to_col else self.move_ne
            out = dir(fr_row, fr_col)
        elif fr_row < to_row:
            dir = self.move_sw if fr_col > to_col else self.move_se
            out = dir(fr_row, fr_col)
        return dir(row, col), out


    def remove_captured_stones_diag(self, fr_row, to_row, fr_col, to_col, 
        row, col):
        """
        Removes any overlapped stones (BLK or WHT)
        in path of piece movement (NE, SE, SW or NW)
        """
        check_sq = {}

        dir,out = self.determine_move_direction(self, fr_row, to_row, fr_col, to_col, 
        row, col)     

        check_sq['sq_1'] = self._board[dir['start_row']][dir['start_col']]
        check_sq['sq_2'] = self._board[dir['r_1']][dir['c_1']]
        check_sq['sq_3'] = self._board[dir['r_2']][dir['c_2']]       
        check_sq['sq_4'] = self._board[dir['r_4']][dir['c_4']]
        check_sq['sq_5'] = self._board[dir['r_5']][dir['c_5']]

        for r, c in [('start_row', 'start_col'), ('r_2', 'c_2'), ('r_1', 'c_1'), ('r_4', 'c_4'), ('r_5', 'c_5')]:
            if self._board[out[r]][out[c]] == 'B' and (dir[r] in (0, 19) or dir[c] in (0, 19)):
                self._blk_stones_left -= 1
            elif self._board[out[r]][out[c]] == 'W' and (dir[r] in (0, 19) or dir[c] in (0, 19)):
                self._wht_stones_left -= 1
            
        for sq in check_sq:
            
            if check_sq[sq] == 'B':
                self._blk_stones_left -= 1
                check_sq[sq] = ''  

            elif check_sq[sq] == 'W':
                self._wht_stones_left -= 1
                check_sq[sq] = ''         
                
            else:
                continue

        return check_sq


    def move_vert(self, fr_row, fr_col, to_row, to_col, board, start_row, 
    window):
        """
        Takes in strings representing coordinates of starting
        and destination squares and current board state. Moves
        piece either North or South if move is valid.
        """

        # window = 3 if fr_square is empty or 16 if not      
        if 1 <= abs(to_row-fr_row) <= window:

            # ptr tracks if stone is in path of move
            # starts at 1st row from starting square
            ptr = start_row 

            while ptr != to_row: # until destination reached
                
                if fr_row > to_row and board[fr_row-1][fr_col] != '':  # move N
                    ptr -= 1  # 1st row beyond piece
                    final_row = ptr+1
                    dir = 'N'
                    beg_row = ptr
                    end_row = ptr-1
                elif fr_row < to_row and board[fr_row+1][fr_col] != '':  # move S        
                    ptr += 1  # 1st row beyond piece
                    final_row = ptr-1
                    dir = 'S'
                    beg_row = ptr
                    end_row = ptr+1
                else:
                    return False

                for j in range(fr_col-1,fr_col+2):

                    # finalize move if moving 1 space from origin
                    if  to_row == start_row and to_col == fr_col:
               
                        # then stop; remove overlapped stones
                        self.remove_captured_stones_vert(start_row, beg_row, end_row, j)

                        # finalize move
                        self.update_board(fr_row, fr_col, to_row, to_col)
                        return True
                    
                    # if stone(s) in path, 
                    if board[ptr][j] != '':
                        
                        # then stop; remove overlapped stones; 
                        self.remove_captured_stones_vert(start_row, beg_row, end_row, j)
                        
                        # finalize move
                        self.update_board(fr_row, fr_col, final_row,to_col)
                        return True

                    # if destination reached
                    if  to_row == ptr and to_col == j:

                        if dir == 'S':
                            # then stop; remove overlapped stones; 
                            self.remove_captured_stones_vert(start_row, ptr, ptr+2, j)
                        else:
                            self.remove_captured_stones_vert(start_row, ptr-1, ptr+1, j)
                        
                        # update board positions with new piece 
                        self.update_board(fr_row, fr_col, to_row, to_col)
                        return True
            
            if fr_row > to_row:
                    # then stop; remove overlapped stones; 
                    self.remove_captured_stones_vert(start_row, ptr-1, ptr, fr_col)
            else: 
                    self.remove_captured_stones_vert(start_row, ptr+1, ptr+2, fr_col)
                
            # finalize move if moving 1 space from origin
            self.update_board(fr_row, fr_col, to_row, to_col)
            return True
        else:        
            # movement not vertical
            return False
        

    def move_horiz(self, fr_row, fr_col, to_row, to_col, board, start_col, window):
        """
        Takes in strings representing coordinates of starting
        and destination squares and current board state. Moves
        piece either East or West if move is valid.
        """

        # check if there is a stone in W or E position
        if any(board[fr_row][c] for c in (fr_col-1, fr_col+1)):
            
            # check if move is within range and in the same row
            if abs(to_col - fr_col) in range(1, window+1) and to_row == fr_row:

                # determine direction of move
                direction = 1 if to_col > fr_col else -1

                # check if any stones are in the way
                for col in range(fr_col + direction, to_col + direction, direction):
                    if board[fr_row][col] != '':
                        self.remove_captured_stones_horiz(start_col, fr_row, fr_col + direction, col - direction)
                        self.update_board(fr_row, fr_col, fr_row, col - direction)
                        return True
                
                # remove overlapped stones and make the move
                self.remove_captured_stones_horiz(start_col, fr_row, to_col, fr_col + direction)
                self.update_board(fr_row, fr_col, to_row, to_col)
                return True
                
        return False

        
    def move_nw(self, row, col):
        """
        Returns a dictionary containing the coordinates of the 
        spaces to which a piece can move in the northeast direction
        from the given row and column.
        """
        return {
            'start_row': row - 1,
            'start_col': col - 1,
            'final_row': row,
            'final_col': col,
            'r_1': row,
            'c_1': col + 1,
            'r_2': row,
            'c_2': col + 2,
            'r_4': row + 1,
            'c_4': col,
            'r_5': row + 2,
            'c_5': col
        }


    def move_ne(self, row, col):
        """
        Returns a dictionary containing the coordinates of the 
        spaces to which a piece can move in the northeast direction
        from the given row and column.
        """
        row -= 1
        col += 1
        return {
            'start_row': row,
            'start_col': col,
            'final_row': row + 1,
            'final_col': col - 1,
            'r_1': row,
            'c_1': col - 2,
            'r_2': row,
            'c_2': col - 1,
            'r_4': row + 1,
            'c_4': col,
            'r_5': row + 2,
            'c_5': col
        }

    
    def move_se(self, row, col):
        """
        Returns a dictionary containing the coordinates of the 
        spaces to which a piece can move in the southeast direction
        from the given row and column.
        """
        row, col = row + 1, col + 1
        return {
            'start_row': row,
            'start_col': col,
            'final_row': row - 1,
            'final_col': col - 1,
            'r_1': row,
            'c_1': col - 2,
            'r_2': row,
            'c_2': col - 1,
            'r_4': row - 1,
            'c_4': col,
            'r_5': row - 2,
            'c_5': col
        }
    

    def move_sw(self, row, col):
        """
        Returns a dictionary containing the coordinates of the spaces 
        to which a piece can move in the southwest direction from the 
        given row and column.
        """
        row, col = row + 1, col - 1
        return {
            'start_row': row,
            'start_col': col,
            'final_row': row - 1,
            'final_col': col + 1,
            'r_1': row,
            'c_1': col + 2,
            'r_2': row,
            'c_2': col + 1,
            'r_4': row - 1,
            'c_4': col,
            'r_5': row - 2,
            'c_5': col
        }


    def determine_diagonal_move_direction(self, fr_row, fr_col, to_row, to_col):
        """
        Returns map of the direction.
        """
        moves = { (True, True): self.move_nw,
                (True, False): self.move_ne,
                (False, False): self.move_se,
                (False, True): self.move_sw }
        
        direction = moves[(fr_row > to_row, fr_col > to_col)]
        return direction
    

    def move_diag(self, fr_row, fr_col, to_row, to_col, board, start_row, start_col):
        """
        Move a piece if valid coordinates and board state are given.
        """

        # check if piece is in SW, SE, NE, or NW position
        if any(board[r][c] for r, c in [(fr_row-1, fr_col-1), (fr_row-1, fr_col+1), \
                (fr_row+1, fr_col+1), (fr_row+1, fr_col-1)]):
                            
            # check if move is diagonal
            if abs(to_col - fr_col) == abs(to_row - fr_row):
                
                direction = self.determine_diagonal_move_direction()

                # check if move is valid and update board
                move = direction(start_row, start_col)

            if all(board[r][c] == '' for r, c in [(move['start_row'], move['start_col']), (move['r_1'], move['c_1']),
                                       (move['r_2'], move['c_2']), (move['r_4'], move['c_4']), (move['r_5'], move['c_5'])]):
                self.remove_captured_stones_diag(fr_row, to_row, fr_col, to_col, move['final_row'], move['final_col'])
                self.update_board(fr_row, fr_col, move['final_row'], move['final_col'])
                return True

        return False


    def get_allowable_range_for_move(self, fr_row, fr_col, board):
        """
        Check if center of piece has stone. 
        Return max allowable range for move.
        """
        return 3 if not board[fr_row][fr_col] else 16

    
    def set_move_direction(self, fr, to):
        """
        Determines the direction of movement and 
        returns the starting index for tracking piece movement.
        """
        if fr < to:
            return fr + 1
        elif fr > to:
            return fr - 1
        else:
            return None


    def prepare_move(self, fr_row, fr_col, to_row, to_col, board):
        """
        Determine movement limits and direction.
        Move piece in given direction.
        """
        window = self.get_allowable_range_for_move(fr_row, fr_col, board)
        start_row = self.set_move_direction(fr_row, to_row)
        start_col = self.set_move_direction(fr_col, to_col)

        if fr_col == to_col:  # can move N or S
            return self.move_vert(fr_row, fr_col, to_row, to_col, board, start_row, window)

        elif fr_row == to_row:  # can move E or W
            return self.move_horiz(fr_row, fr_col, to_row, to_col, board, start_col, window)

        else:  # can move NW, NE, SW or SE
            return self.move_diag(fr_row, fr_col, to_row, to_col, board, start_row, start_col)
    

    def check_for_ring(self):
        """
        Checks for the presence of rings on the board.
        Updates the total for each player.
        """

        # start at first square top left corner of board
        i = 0  # row i on board
        j = 0  # column j on board

        # set ring counters to 0 for each player
        self._blk_rings_left = 0
        self._wht_rings_left = 0

        # check each square for the presence of a piece and
        # determine if a ring pattern is formed for each piece
        board = self.get_game_board()

        while i <= 17 and j <= 17:

            # store the value of first element
            ring_element = board[i][j]

            # 2nd element is equal to row, col + 1
            if board[i][j + 1] == ring_element:

                # 3rd element is equal to row, col + 2
                if board[i][j + 2] == ring_element:

                    # 4th element is row + 1, col
                    if board[i + 1][j] == ring_element:

                        # 5th element is empty row + 1, col + 1
                        if board[i + 1][j + 1] == '':

                            # 6th element is row + 1, col + 2
                            if board[i + 1][j + 2] == ring_element:

                                # 7th element is row + 2, col
                                if board[i + 2][j] == ring_element:

                                    # 8th element is row + 2, col + 1
                                    if board[i + 2][j + 1] == ring_element:

                                        # 9th element is row + 2, col + 2
                                        if board[i + 2][j + 2] == ring_element:
                                            if ring_element == 'W':
                                                self._wht_rings_left += 1
                                            elif ring_element == 'B':
                                                self._blk_rings_left += 1
                                            else:
                                                pass

            j += 1  # check the next column incrementally

            # move to next row after each column checked
            if j == 18:
                i = i + 1
                j = 0
            
        return self._blk_rings_left, self._wht_rings_left


    def track_pc_count(self):
        """
        Tracks the count of black and white stones on board.
        """
        self._blk_stones_left = sum(row.count('B') for row in self.get_game_board())
        self._wht_stones_left = sum(row.count('W') for row in self.get_game_board())
        
        return self._blk_stones_left, self._wht_stones_left


    def make_move(self, fr_square, to_square):
        """
        Update game by moving a piece from the provided starting 
        square to the destination square if valid.
        """

        # starting and destination coords. conversion to int
        fr_col, fr_row = self._alpha_to[fr_square[0].lower()], int(fr_square[1:]) - 1
        to_col, to_row = self._alpha_to[to_square[0].lower()], int(to_square[1:]) - 1

        self.set_ftprint(fr_row, fr_col)

        # check move validity - move if legal
        if not self.is_move_legal(fr_row, to_row, fr_col, to_col):
            print("Illegal move. Try again.")
            return False

        # continue if game has not been won, otherwise stop and return False
        if self.get_game_state() != 'UNFINISHED':
            print("Game over.", self.get_game_state())
            return False

        # set move based on position of stones in footprint
        if self.prepare_move(fr_row, fr_col, to_row, to_col, self.get_game_board()):

            # check if rings are on board
            self.check_for_ring()

            # set game state based on ring count
            if self._blk_rings_left == 0:
                self._current_state = 'WHITE WON'
            elif self._wht_rings_left == 0:
                self._current_state = 'BLACK WON'

            # update player and set previous move
            self._prev_move, self._player_to_move, self._other_player = \
                self._player_to_move, self._other_player, self._prev_move

            return True

        return False


    def player_resign(self):
        """
        Quit. Give other player the win.
        """
        quit = input('Would you like to quit the game (Y or N)?').lower()
        
        if quit == 'y':
            self._current_state = 'WHITE WON' if self._player_to_move == 'B' \
                else 'BLACK WON'
            print(self._current_state)
            return True
        return False


    def print_board(self):
        """Visualization of gameboard."""
        print(*self._board, sep="\n")
