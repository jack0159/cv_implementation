import numpy as np
import cv2 as cv


class Board:
    

    @abstractmethod

    def board_update(self):
        pass

    def board_show(self):
        pass

    
class RawBoard(Board):

    board = []
    mine_n = 0
    flag_n = 0

    def __init__(self, lv):

        self.level = lv
        self.row_n = int(self.level*6*1.2)
        self.col_n = int(self.level*6*0.8)
        
        tile_list = []

        for r in range(self.row_n):
            temp_list = []
            for c in range(self.col_n):
                temp_list.append(Tile(lv, r, c))
            tile_list.append(temp_list)

        self.board = tile_list

        self.display_board = DisplayBoard(lv, cell_size=40)
        self.score_board = ScoreBoard(mine_n, flag_n)




    def numbering_tiles(self, board):

        cnt = 0

        for r in range(self.row_n):
            for c in range(self.col_n):

                if not(board[r, c].is_mine):
                    temp_sum_val = 0
                    for i in [-1, 0, 1]:
                        for j in [-1, 0, 1]:
                            if idx_possible(self.row_n, self.col_n, r,  c):
                                temp_sum_val += board[r + i, c + j]
                            else:
                                continue
                    board[r, c].tile_num = temp_sum_val

                else:
                    board[r, c].tile_num = -1
                    cnt += 1

        self.mine_n = cnt
                    

    def dig(self, idx):

        if self.board[idx].is_opened != True:
            self.board[idx].is_opened = True
        else:
            return
        
        if self.board[idx].tile_num == 0:
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if idx_possible(self.row_n, self.col_n, idx[0] + i, idx[1] + j):
                        self.dig(idx[0] + i, idx[1] + j)

    def set_flag(self, idx):
        if not(self.board[idx].is_opened):
            if not(self.board[idx].is_flagged):
                self.board[idx].is_flagged = True
                self.flag_n += 1
            else:
                self.board[idx].is_flagged = False
                self.flag_n -= 1


    def board_update(self):


    
    


class ScoreBoard:

    def __init__(self, mine_n, flag_n):
        self.mine_left = mine_n
        self.num_of_flags = flag_n




class DisplayBoard:


    def __init__(self, level, cell_size):

        self.row_n = int(level*6*1.2)
        self.col_n = int(level*6*0.8)
        self.board = np.zeros((self.row_n * cell_size, self.col_n * cell_size))

        for r in range(self.row_n):
            for c in range(self.col_n):
                pos = (int(c*cell_size + (cell_size/2)), int(r*cell_size + (cell_size/2)))
                self.board[r*cell_size:(r + 1)*cell_size, c*cell_size:(c + 1)*cell_size] = cv.resize(self.__num2img(self.raw_board[r, c]), (cell_size, cell_size))

    


    


    

class Tile:

    tile_num = 0 # num of surrounding mine, -1 if it's mine
    tile_idx = (0, 0) # tile's index in board
    is_mine = False   
    is_opened = False # If opened --> True, default : False
    is_flagged = False

    def __init__(self, lv, r, c):
        ratio = 0.3 + (lv * 0.01)
        self.is_mine = random_binary(ratio)
        self.tile_idx = (r, c)


    





def random_binary(ratio):
    val = np.random.uniform(low=0, high=1, size=1)[0]
    if val > ratio:
        return 0
    else:
        return 1

def idx_possible(h, w, r, c):
    return not(r >= h or r < 0 or c >= w or c < 0)




def click(event, x, y, flag, param):
    global current_x
    global current_y
    global cursor_type

    if event == cv.EVENT_LBUTTONDOWN:
        current_y = int(y/40)
        current_x = int(x/40)
        cursor_type = 0
    if event == cv.EVENT_RBUTTONDOWN:
        current_y = int(y/40)
        current_x = int(x/40)
        cursor_type = 1




(current_y, current_x) = (-1, -1)
cursor_type = 0



num_dict = {
    1:cv.imread('./image/one.png', cv.IMREAD_GRAYSCALE), 
    2:cv.imread('./image/two.png', cv.IMREAD_GRAYSCALE),
    3:cv.imread('./image/three.png', cv.IMREAD_GRAYSCALE),
    4:cv.imread('./image/four.png', cv.IMREAD_GRAYSCALE),
    5:cv.imread('./image/five.png', cv.IMREAD_GRAYSCALE),
    6:cv.imread('./image/six.png', cv.IMREAD_GRAYSCALE),
    7:cv.imread('./image/seven.png', cv.IMREAD_GRAYSCALE),
    8:cv.imread('./image/eight.png', cv.IMREAD_GRAYSCALE),
    0:cv.imread('./image/zero.png', cv.IMREAD_GRAYSCALE)
}
mine = cv.imread('./image/mine.png', cv.IMREAD_GRAYSCALE)
flag = cv.imread('./image/flag.png', cv.IMREAD_GRAYSCALE)



