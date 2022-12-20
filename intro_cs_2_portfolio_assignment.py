# Bobby Craft
# Date: 6-3-22
# Description: Intro to Comp Sci II: Module 10 Project
#
# Write a class named GessGame for playing an abstract board game 
# called Gess. You can see the rules [here](https://www.chessvariants.com/crossover.dir/gess.html).  
# Note that when a piece's move causes it to overlap stones, any stones covered by the **footprint**
#  get removed, not just those covered by one of the piece's stones.  It is not legal to make a move 
# that leaves you without a ring.  It's possible for a player to have more than one ring.  A player 
# doesn't lose until they have no remaining rings.

# Locations on the board will be specified using columns labeled a-t and rows labeled 1-20, with 
# row 1 being the Black side and row 20 the White side.  The actual board is only columns b-s and 
# rows 2-19.  The center of the piece being moved must stay within those boundaries.  An edge of 
# the piece may go into columns a or t, or rows 1 or 20, but any pieces there are removed at the 
# end of the move.  Black goes first.

# There's an online implementation [here](https://gess.h3mm3.com/) you can try, but it's not 100% 
# consistent with the rules. In the case of any discrepancy between the online game and the rules, 
# you should comply with the rules (you can also ask us for clarification of course).  One example 
# is that the online game lets you make moves that leave you without a ring, which isn't allowed 
# (if a player wants to end the game, they can just resign).  Another example is that the online 
# game lets you choose a piece whose center is off the board (in columns a or t, or in rows 1 or 20), 
# which isn't allowed.

# You're not required to print the board, but you will probably find it very useful for testing 
# purposes.

# Your GessGame class must include the following:
# * An init method that initializes any data members.
# * A method called get_game_state that takes no parameters and returns 'UNFINISHED', 'BLACK_WON' 
# or 'WHITE_WON'.
# * A method called resign_game that lets the current player concede the game, giving the other 
# player the win.
# * A method called make_move that takes two parameters - strings that represent the center square 
# of the piece being moved and the desired new location of the center square.  For example, make_move
# ('b6', 'e9').  If the indicated move is not legal for the current player, or if the game has already 
# been won, then it should just return False.  Otherwise it should make the indicated move, remove any 
# captured stones, update the game state if necessary, update whose turn it is, and return True.

# Feel free to add whatever other classes, methods, or data members you want.  All data members must 
# be **private**.

# # Here's a very simple example of how the class could be used:
# ```
# game = GessGame()
# move_result = game.make_move('m3', 'm6')
# game.make_move('e14', 'g14')
# state = game.get_game_state()
# game.resign_game()

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
        Sets-up go board where the keys are the square 
        coordinates and the values are either the stone 
        ('BLK' or 'WHT') occupying the square or an empty 
        square('').
        """
        self._board = GoBoard()._game_board

        for stone in GoBoard()._black_stones:
            col = self._alpha_to[stone[0].lower()]  # positions to int
            row = int(stone[1:]) - 1
            self._board[row][col] = 'B'  # assign blk stone to square

        for stone in GoBoard()._white_stones:
            col_w = self._alpha_to[stone[0]]  # postions to int
            row_w = int(stone[1:]) - 1
            self._board[row_w][col_w] = 'W'  # assign wht stone to square

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

        self._ftprint[1][1] = board[fr_row][fr_col]
        self._ftprint[2][1] = board[fr_row + 1][fr_col]
        self._ftprint[0][1] = board[fr_row - 1][fr_col]
        self._ftprint[1][2] = board[fr_row][fr_col + 1]
        self._ftprint[1][0] = board[fr_row][fr_col - 1]
        self._ftprint[2][2] = board[fr_row + 1][fr_col + 1]
        self._ftprint[0][2] = board[fr_row - 1][fr_col + 1]
        self._ftprint[2][0] = board[fr_row + 1][fr_col - 1]
        self._ftprint[0][0] = board[fr_row - 1][fr_col - 1]

        return self._ftprint


    def update_fr_position(self,fr_row, fr_col, board):
        """
        Empties ('') orign squares covered 
        by 3x3 piece to prep for move.  
        """

        board[fr_row][fr_col] = ''
        board[fr_row-1][fr_col] = ''
        board[fr_row+1][fr_col] = ''
        board[fr_row][fr_col-1] = ''
        board[fr_row-1][fr_col-1] = ''
        board[fr_row+1][fr_col-1] = ''
        board[fr_row-1][fr_col+1] = ''
        board[fr_row][fr_col+1] = ''
        board[fr_row+1][fr_col+1] = ''


    def update_to_position(self,to_row, to_col, board, ftprint):
        """
        Updates board destination squares after 3x3 
        footprint moves. Captures any stones occupying
        destination squares.
        """

        board[to_row][to_col] = ftprint[1][1]
        board[to_row-1][to_col] = ftprint[0][1]
        board[to_row+1][to_col] = ftprint[2][1]
        board[to_row][to_col-1] = ftprint[1][0]
        board[to_row-1][to_col-1] = ftprint[0][0]
        board[to_row+1][to_col-1] = ftprint[2][0]
        board[to_row-1][to_col+1] = ftprint[0][2]
        board[to_row][to_col+1] = ftprint[1][2]
        board[to_row+1][to_col+1] = ftprint[2][2]


    def update_board(self,fr_row, fr_col, to_row, to_col):
        """
        Updates board after moving piece.  As soon as the footprint 
        overlaps other stones (of either color), movement stops 
        and all stones that were overlapped are removed permanently 
        from the game. 
        """

        self.update_fr_position(fr_row, fr_col, self._board)
        self.update_to_position(to_row, to_col, self._board, 
        self.get_ftprint()) 

        return self._board


    def check_if_players_turn(self, fr_space, to_space):
        """
        Takes in strings representing the location to move from and 
        the location to move to.  Checks if move is allowed and it's
        current player's turn to move. If so, returns True, otherwise 
        False.
        """
        if self.make_move(fr_space, to_space): # if move legal
            if self._player_to_move == self._prev_move:
                print("It's the other player's turn! >:-<")
                return False
            return True
        return False
    

    def is_piece_legal(self):
        """
        Checks if piece legal. If squares surrounding 
        center of 3x3 matix empty or matrix contains other 
        player's stone, return False. Otherwise piece is 
        legal, return True.
        """
        legal = False

        # if other player's stone at center, piece is invalid  
        if self.get_ftprint()[1][1] == self._other_player:
            return False

        # otherwise, check squares surrounding center
        for i in range(0, 3):
            for j in range(0,3):          
                # skip, only check surrounding squares
                if i == 1 and j == 1:
                    continue
                # invalid: if other players's stone found
                if self.get_ftprint()[i][j] == self._other_player:
                    return False
                # valid: if only current player's stone found
                if self.get_ftprint()[i][j] == self._player_to_move:
                    legal = True
        # invalid: if no current player's stones found
        return legal       
            

    def is_move_legal(self, fr_row, to_row, fr_col, to_col):
        """
        Takes in strings representing starting location 
        and destination. Returns True if valid move, 
        False otherwise.
        """
        # don't move if piece invalid
        if not self.is_piece_legal(): 
            return False

        # destination square equals starting square
        if to_row == fr_row and to_col == fr_col:
            return False

        # destination square is out-of-bounds
        if 18 < to_row < 1 or 18 < to_col < 1:
            return False

        # starting square is out-of-bounds
        if 18 < fr_row < 1 or 18 < fr_col < 1:
            return False    
         
        return True
    

    def remove_captured_stones_vert(self, start_row, beg_row, end_row, fr_col):
        """
        Removes any overlapped stones (BLK or WHT)
        in path of piece movement (N or S)
        """
        
        for row in range(beg_row, end_row):
            for col in range(fr_col-1,fr_col+2):
            
                if row == 0 or row == 19:
                    if self.get_game_board()[start_row][col] == 'B':
                        self._blk_stones_left -= 1
                    if self.get_game_board()[start_row][col] == 'W':
                        self._wht_stones_left -= 1

                if self.get_game_board()[row][col] == 'B':
                    self._blk_stones_left -= 1
                    self.get_game_board()[row][col] = ''
                
                if self.get_game_board()[row][col] == 'W':
                    self._wht_stones_left -= 1
                    self.get_game_board()[row][col] = ''
                
                else:
                    continue
                
        return self.get_game_board()

    
    def remove_captured_stones_horiz(self, start_col, row, beg_col, end_col):
        """
        Removes any overlapped stones (BLK or WHT)
        in path of piece movement (E or W)
        """

        for row in range(row-1, row+2):
            for col in range(beg_col, end_col):
                
                if col == 0 or col == 19:       
                    if self.get_game_board()[row][start_col] == 'B':
                        self._blk_stones_left -= 1
                    if self.get_game_board()[row][start_col] == 'W':
                        self._wht_stones_left -= 1
                             
                if self.get_game_board()[row][col] == 'B':
                    self._blk_stones_left -= 1
                    self.get_game_board()[row][col] = ''
                                
                if self.get_game_board()[row][col] == 'W':
                    self._wht_stones_left -= 1
                    self.get_game_board()[row][col] = ''
                
                else:
                    continue
                
        return self.get_game_board()
    
    def remove_captured_stones_diag(self, fr_row, to_row, fr_col, to_col, 
        row, col):
        """
        Removes any overlapped stones (BLK or WHT)
        in path of piece movement (NE, SE, SW or NW)
        """
        check_sq = {}

        if fr_row > to_row and fr_col > to_col:
            dir = self.move_nw(row,col)
            out = self.move_nw(fr_row,fr_col)
       
        if fr_row > to_row and fr_col < to_col:
            dir = self.move_ne(row,col)
            out = self.move_ne(fr_row,fr_col)

        if fr_row < to_row and fr_col > to_col:
            dir =self.move_sw(row,col)
            out = self.move_sw(fr_row,fr_col)

        if fr_row < to_row and fr_col < to_col:
            dir = self.move_se(row,col)
            out = self.move_se(fr_row,fr_col) 

        check_sq['sq_1'] = self._board[dir['start_row']][dir['start_col']]
        check_sq['sq_2'] = self._board[dir['r_1']][dir['c_1']]
        check_sq['sq_3'] = self._board[dir['r_2']][dir['c_2']]       
        check_sq['sq_4'] = self._board[dir['r_4']][dir['c_4']]
        check_sq['sq_5'] = self._board[dir['r_5']][dir['c_5']]

        if self._board[out['start_row']][out['start_col']] == 'B':
            if dir['start_row'] == 0 or dir['start_row'] == 19 or \
                dir['start_col'] == 0 or dir['start_col'] == 19:
                self._blk_stones_left -=1

        if self._board[out['r_2']][out['c_2']] == 'B':
            if dir['r_2'] == 0 or dir['r_2'] == 19 or \
                dir['c_2'] == 0 or dir['c_2'] == 19:
                self._blk_stones_left -=1

        if self._board[out['r_1']][out['c_1']] == 'B':
            if dir['r_1'] == 0 or dir['r_1'] == 19 or \
                dir['c_1'] == 0 or dir['c_1'] == 19:
                self._blk_stones_left -=1

        if self._board[out['r_4']][out['c_4']] == 'B':
            if dir['r_4'] == 0 or dir['r_4'] == 19 or \
                dir['c_4'] == 0 or dir['c_4'] == 19:
                self._blk_stones_left -=1

        if self._board[out['r_5']][out['c_5']] == 'B':
            if dir['r_5'] == 0 or dir['r_5'] == 19 or \
                dir['c_5'] == 0 or dir['c_5'] == 19:
                self._blk_stones_left -=1

        if self._board[out['start_row']][out['start_col']] == 'W':
            if dir['start_row'] == 0 or dir['start_row'] == 19 or \
                dir['start_col'] == 0 or dir['start_col'] == 19:
                self._wht_stones_left -=1

        if self._board[out['r_2']][out['c_2']] == 'W':
            if dir['r_2'] == 0 or dir['r_2'] == 19 or \
                dir['c_2'] == 0 or dir['c_2'] == 19:
                self._wht_stones_left -=1

        if self._board[out['r_1']][out['c_1']] == 'W':
            if dir['r_1'] == 0 or dir['r_1'] == 19 or \
                dir['c_1'] == 0 or dir['c_1'] == 19:
                self._wht_stones_left -=1

        if self._board[out['r_4']][out['c_4']] == 'W':
            if dir['r_4'] == 0 or dir['r_4'] == 19 or \
                dir['c_4'] == 0 or dir['c_4'] == 19:
                self._wht_stones_left -=1

        if self._board[out['r_5']][out['c_5']] == 'W':
            if dir['r_5'] == 0 or dir['r_5'] == 19 or \
                dir['c_5'] == 0 or dir['c_5'] == 19:
                self._wht_stones_left -=1
            
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

        # if stone in N or S position
        # if board[fr_row+1][fr_col] != '' or board[fr_row-1][fr_col] != '':
                    
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
                        
                        # finalize move
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

        # if stone in W or E position
        if board[fr_row][fr_col-1] != '' or  board[fr_row][fr_col+1] != '':
                        
            # valid move if within range        
            if 1 <= abs(to_col-fr_col) <= window and fr_row == to_row:

                # ptr tracks if stone is in path of move
                # starts at 1st column from starting square
                j = start_col

                while j != to_col:
                    # move W
                    if fr_col > to_col and board[fr_row][fr_col-1] != '':
                        j -= 1
                        final_col = j+1
                        dir = 'W'
                        beg_col = j
                        end_col = j-1
                    # move E
                    if fr_col < to_col and board[fr_row][fr_col+1] != '':
                        j += 1
                        final_col = j-1
                        dir = 'E'
                        beg_col = j
                        end_col = j+1

                    for i in range(fr_row-1,fr_row+2):
                        if  to_col == start_col and to_row == fr_row:
                            # then stop; remove overlapped stones
                            self.remove_captured_stones_horiz(start_col, i, beg_col, end_col)
                            
                            # finalize move
                            self.update_board(fr_row, fr_col, to_row, to_col)
                            return   

                        # if stone(s) in path, then stop; remove 
                        # overlapped stones; and finalize move 
                        if board[i][j] != '':
                            # then stop; remove overlapped stones
                            self.remove_captured_stones_horiz(start_col, i, beg_col, end_col)
                            
                            # finalize move
                            self.update_board(fr_row, fr_col, final_col,to_col)
                            return True

                        # finalize move if destination reached  
                        if  to_row == i and to_col == j:

                            if dir == 'E':

                                # then stop; remove overlapped stones; 
                                self.remove_captured_stones_horiz(start_col, i, j, j+2)

                            else:
                                self.remove_captured_stones_horiz(start_col, i, j, j-2)
                                                        
                            # finalize move
                            self.update_board(fr_row, fr_col, to_row, to_col)
                            return True
                # If move is E
                if fr_col > to_col:
                    # Stop; remove overlapped stones
                    self.remove_captured_stones_horiz(start_col, fr_row, j-1, j)
                # Else move is W; Remove overlapped stones
                else: 
                    self.remove_captured_stones_horiz(start_col, fr_row, j+1, j+2)

                # finalize move if moving 1 space from origin
                self.update_board( fr_row, fr_col, to_row, to_col)
                return True
        return False
        
 
    def move_nw(self, row,col):
        nw = {}
        row -= 1
        nw['final_row'] = row+1
        col -= 1
        nw['final_col'] = col+1
        nw['start_row'], nw['start_col'] = row, col
        nw['r_1'], nw['c_1'] = row, col+1
        nw['r_2'], nw['c_2'] = row, col+2
        nw['r_4'], nw['c_4'] = row+1, col
        nw['r_5'], nw['c_5'] = row+2, col

        return nw
    

    def move_ne(self, row,col):
        ne = {}
        row -= 1

        ne['final_row'] = row+1
        col += 1
        ne['final_col'] = col-1
        ne['start_row'], ne['start_col'] = row, col
        ne['r_1'], ne['c_1'] = row, col-2
        ne['r_2'], ne['c_2'] = row, col-1
        ne['r_4'], ne['c_4'] = row+1, col
        ne['r_5'], ne['c_5'] = row+2, col 

        return ne
    

    def move_se(self, row,col):
        se = {}
        row += 1
        se['final_row'] = row-1
        col += 1
        se['final_col'] = col-1
        se['start_row'], se['start_col'] = row, col
        se['r_1'], se['c_1'] = row, col-2
        se['r_2'], se['c_2'] = row, col-1
        se['r_4'], se['c_4'] = row-1, col
        se['r_5'], se['c_5'] = row-2, col

        return se
    

    def move_sw(self, row,col):
        sw = {}
        row += 1
        sw['final_row'] = row-1
        col -= 1
        sw['final_col'] = col+1
        sw['start_row'], sw['start_col'] = row, col
        sw['r_1'], sw['c_1'] = row, col+2
        sw['r_2'], sw['c_2'] = row, col+1
        sw['r_4'], sw['c_4'] = row-1, col
        sw['r_5'], sw['c_5'] = row-2, col

        return sw
                       
                       
    def move_diag(self, fr_row, fr_col, to_row, to_col, board, start_row, start_col):
        """
        Takes in strings representing coordinates of starting
        and destination squares and current board state. Moves
        piece either SW, SE, NW, or NE if move is valid.
        """
        # if stone in SW, SE, NE, or NW position
        if board[fr_row-1][fr_col-1] or board[fr_row-1][fr_col+1] or board[fr_row+1][fr_col+1] or board[fr_row+1][fr_col-1] != '':
                        
            # valid move if within range          
            if abs(to_col - fr_col) == abs(to_row - fr_row):

                i, j = start_row, start_col
                
                while i != to_row and j != to_col:

                    # move nw
                    if fr_row > to_row and fr_col > to_col:
                        dir = self.move_nw(i,j)
                        i -= 1
                        j -= 1
                        
                    # move ne                    
                    if fr_row > to_row and fr_col < to_col:
                        dir = self.move_ne(i,j)
                        i -= 1
                        j += 1
                                              
                    # move se
                    if fr_row < to_row and fr_col < to_col:
                        dir = self.move_se(i,j)
                        i += 1
                        j += 1

                    # move sw
                    if fr_row < to_row and fr_col > to_col:
                        dir = self.move_sw(i,j)
                        i += 1
                        j -= 1
                         
                    if board[dir['start_row']][dir['start_col']] or board[dir['r_1']][dir['c_1']] or board[dir['r_2']][dir['c_2']] or \
                        board[dir['r_4']][dir['c_4']] or board[dir['r_5']][dir['c_5']] != '':
                        self.remove_captured_stones_diag(fr_row, to_row, fr_col, to_col, i,j)
                        self.update_board(fr_row, fr_col, dir['final_row'], dir['final_col'])
                        return True
                    
                    if i == to_row and j == to_col:
                        self.remove_captured_stones_diag(fr_row, to_row, fr_col, to_col, i, j)
                        self.update_board(fr_row, fr_col, i, j)
                        return True
                
                self.remove_captured_stones_diag(fr_row, to_row, fr_col, to_col, i, j)
                self.update_board(fr_row, fr_col, i, j)  
                return True

        return False  
    

    def get_allowable_range_for_move(self, fr_row, fr_col, board):
        """
        Check if center of piece has stone. 
        Return max allowable range for move.
        """

        # if no stone, max move = 3 spaces  
        if board[fr_row][fr_col] == '':   
            window = 3  

        # if stone, max move = 16 spaces
        elif board[fr_row][fr_col] != '':
            window = 16
        
        return window
    
    def set_move_vert_direction(self, fr_row, to_row):
        """
        Dertermine direction of vertical movement.  
        Return starting row for tracking piece movement.
        """
        start_row = None 
        
        # prepare S move 
        if fr_row < to_row:
            start_row = fr_row+1

        # prepare N move 
        if fr_row > to_row:
            start_row = fr_row-1
        
        return start_row
    

    def set_move_horiz_direction(self, fr_col, to_col):
        """
        Dertermine direction of horizontal movement.  
        Return starting row for tracking piece movement.
        """
        start_col = None
        # prepare E move,
        if fr_col < to_col:
            start_col = fr_col+1 

        # prepare W move
        if fr_col > to_col:
            start_col =fr_col-1 
        
        return start_col

    def prepare_move(self, fr_row, fr_col, to_row, to_col, board):
        """
        Determine movement limits and direction.
        Move piece in given direction.
        """

        window = self.get_allowable_range_for_move(fr_row, fr_col, board)
        start_row = self.set_move_vert_direction(fr_row, to_row)
        start_col = self.set_move_horiz_direction(fr_col, to_col)
       
        # can move N or S
        if fr_col == to_col:
            if self.move_vert(fr_row, fr_col, to_row, to_col, board, start_row, window):
                return True

        # can move E or W
        elif fr_row == to_row:
            if self.move_horiz(fr_row, fr_col, to_row, to_col, board, start_col, window):
                return True

        # can move NW, NE, SW or SE
        elif self.move_diag(fr_row, fr_col, to_row, to_col, board, start_row, start_col):
            return True

        return False
    

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
        Tracks the count of black and white stones
        on board.
        """
        # set counters to 0 for each player
        self._blk_stones_left = 0
        self._wht_stones_left = 0

        for i in self.get_game_board():
            for j in i:
                if j == 'B':
                    self._blk_stones_left += 1
                elif j == 'W':
                    self._wht_stones_left += 1
                else:
                    pass
        return self._blk_stones_left, self._wht_stones_left


    def make_move(self, fr_square, to_square):
        """
        Takes in strings that represent the starting and desired
        destination square for move.  Makes the move, if valid,
        updates game to reflect the move. 
        """
       
       # starting and destination coords. conversion to int
        fr_col, fr_row  = self._alpha_to[fr_square[0].lower()], int(fr_square[1:]) - 1
        to_col , to_row = self._alpha_to[to_square[0].lower()], int(to_square[1:]) - 1
        
        self.set_ftprint(fr_row, fr_col)

        # check move validity - move if legal
        if not self.is_move_legal(fr_row, to_row, fr_col, to_col):
            print("Illegal move. Try again.")
            return False

        # continue if game has not been won
        # otherwise, stop and return False
        if self.get_game_state() != 'UNFINISHED':
            print("Game over.", self.get_game_state())
            return False

        # set move based on position of stones in footprint:

        if self.prepare_move(fr_row, fr_col, to_row, to_col, self.get_game_board()):
        
            # check if rings are on board
            self.check_for_ring()

            # if player BLK has no rings, WHT player wins
            if self._blk_rings_left == 0:
                self._current_state = 'WHITE WON'
                print(self.get_game_state())

            # if player WHT has no rings, BLK player wins
            elif self._wht_rings_left == 0:
                self._current_state = 'BLACK WON'
                print(self.get_game_state())

            else:
                pass

            # update player and set previous move
            self._prev_move = self._player_to_move
            self._player_to_move = self._other_player
            self._other_player = self._prev_move

            return True
        
        return False


    def player_resign(self):
        """
        Quit. Give other player the win.
        """
        quit = str(input('Would you like to quit the game (Y or N)?'))

        if quit.lower() == 'y':

            if self._player_to_move == 'B':
                self._current_state = 'WHITE WON'
                print(self._current_state)
                return True

            elif self._player_to_move == 'W':
                self._current_state = 'BLACK WON'
                print(self._current_state)
                return True

        return False


    def print_board(self):
        """
        Visualization of gameboard.
        """
        for i in self._board:
            print(i)


game = GessGame()
game.set_game_board()
# game.print_board()
# game.make_move('c6', 'c9') # vert blk'
# game.make_move('c15', 'c12') # vert wht'
# game.make_move('c9','c11') # vert blk'
# game.make_move('f15', 'f12')
# game.check_if_players_turn('f15', 'f12')
# game.make_move('b11', 'e11')
# game.make_move('j15', 'g12')
# game.make_move('c3', 'd3')
# game.make_move('g12', 'd9')
# game.make_move('g6', 'd9')
# game.make_move('f18', 'e17')
# game.make_move('r3', 'r5')
# game.make_move('e17', 'n8')
# game.make_move('k6', 'l7')
# game.make_move('o8', 'n8')
# game.make_move('r6', 'r5')
# game.make_move('i18', 'i8')
# game.make_move('r5', 'r13')
# game.make_move('i8', 'e8')
# game.make_move('s12', 'r13')
# game.make_move('e8', 'd9')
# game.make_move('d3', 'd7')
# game.make_move('d10', 'e9')
# game.make_move('i3', 'i18')
# game.make_move('n8', 'n5')
# game.make_move('r3', 's3')
# game.get_game_stone_count()
game.print_board()

# print(game.get_blk_ring_counter())
# print(game.get_wht_ring_counter())







move_result = game.make_move('m3', 'm6')
game.make_move('e14', 'g14')
state = game.get_game_state()
# game.player_resign()