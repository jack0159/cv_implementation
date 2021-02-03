import numpy as np
import cv2 as cv

class MineSweeper:

    ## Attributes


    display_board = None
    raw_board = None

    level = None
    row_n = None
    col_n = None

    is_over = False

    mine_n = 0
    opened_n = 0


    

    def __init__(self):

        self.level = int(input("Select Level : "))

        self.set_size()
        self.display_board = DisplayBoard(self, 40)
        self.create_raw_board()
        self.numbering_tiles(self.raw_board)
        


    def player_win(self):
        return self.row_n * self.col_n - self.mine_n == self.opened_n


    ## Initializing Functions

    # set raw_board's size by level
    def set_size(self):
        self.row_n = int(self.level * 8 * 0.8)
        self.col_n = int(self.level * 8 * 1.2)

    # fill the raw_board with Tiles
    def create_raw_board(self):

        # empty Tile list
        tile_list = []

        for r in range(self.row_n):
            temp_list = []
            for c in range(self.col_n):

                temp_list.append(Tile(self))

            tile_list.append(temp_list)

        self.raw_board = tile_list
        
    def numbering_tiles(self, raw_board):

        # parameter for number of mines
        cnt = 0

        # Search all raw_board
        for r in range(self.row_n):
            for c in range(self.col_n):

                # If the tile is not mine tile, compute the number of surrounding mines
                if not(self.raw_board[r][c].is_mine):
                    temp_sum_val = 0
                    for i in [-1, 0, 1]:
                        for j in [-1, 0, 1]:
                            if idx_possible(self.row_n, self.col_n, r + i,  c + j):
                                temp_sum_val += raw_board[r + i][c + j].is_mine
                            else:
                                continue
                    raw_board[r][c].tile_num = temp_sum_val

                # If the tile is mine tile, set -1
                else:
                    raw_board[r][c].tile_num = -1
                    cnt += 1

        # Counting mines
        self.mine_n = cnt
                    
    ## Action Functions

    def dig(self, idx):

        (y, x) = idx

        # If tile is not opened, open it
        if not(self.raw_board[y][x].is_opened):

            # If it's mine, Game Over
            if self.raw_board[y][x].is_mine:
                self.is_over = True
                return

            # If it's not a mine, open it
            else:
                self.raw_board[y][x].is_opened = True

                # Count opened Tiles
                self.opened_n += 1
            
        # If tile was already opened, function exit
        else:
            return


        # If tile number is 0, open surrounding 0 tiles recursively
        if self.raw_board[y][x].tile_num == 0:
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if idx_possible(self.row_n, self.col_n, y + i, x + j):
                        self.dig((y + i, x + j))

    def flag_set_or_remove(self, idx):

        global left_click

        (y, x) = idx

        # You can only set flag on unpoened tiles
        if not(self.raw_board[y][x].is_opened):

            # If there's no flag, set flag
            if not(self.raw_board[y][x].is_flagged):
                self.raw_board[y][x].is_flagged = True

                left_click = True

            # If there's flag, remove it
            else:
                self.raw_board[y][x].is_flagged = False

                left_click = True

        


    ## Update Function

    def update(self):

        global current_x

        if current_x != -1:
            if left_click:
                self.dig((current_y, current_x))
            else:
                self.flag_set_or_remove((current_y, current_x))

        current_x = -1


    def game_start(self):

        # Interface#############################
        print("\nLClick : Open")
        print("RClick : Flag\n") 
        ########################################
        
        while True:

            self.update()
            self.display_board.display(self)

            if self.player_win():
                print('You Won')
                break
            elif self.is_over:
                print('Game Over')
                break

            elif cv.waitKey(1) == 27:
                break
        


class DisplayBoard:

    cell_size = None
    height = None
    width = None
    showing_board = None

    def __init__(self, MineSweeper, cell_size):

        self.cell_size = cell_size

        self.height = MineSweeper.row_n * self.cell_size
        self.width = MineSweeper.col_n * self.cell_size

        self.showing_board = np.zeros((self.height, self.width))

    # Fill the display board with right tile images
    def display(self, MineSweeper):

        c_s = self.cell_size

        for r in range(MineSweeper.row_n):
            for c in range(MineSweeper.col_n):

                self.showing_board[r * c_s : (r + 1) * c_s, c * c_s : (c + 1) * c_s] = MineSweeper.raw_board[r][c].tile_img(img_dict)

        cv.imshow('MineSweeper', self.showing_board)
            
class Tile:

    tile_size = None
    tile_num = None # num of surrounding mine, -1 if it's mine
    is_mine = False   
    is_opened = False # If opened --> True, default : False
    is_flagged = False

    def __init__(self, MineSweeper):
        ratio = 0.2 + (MineSweeper.level * 0.01)
        self.is_mine = random_binary(ratio)
        self.tile_size = MineSweeper.display_board.cell_size

    # return the right image of each tiles
    def tile_img(self, img_set):

        t_s = self.tile_size

        if self.is_opened:
            
            if self.is_mine:
                return cv.resize(img_set['mine'], (t_s, t_s))
            else:
                return cv.resize(img_set[self.tile_num], (t_s, t_s))
        else:

            if self.is_flagged:
                return cv.resize(img_set['flag'], (t_s, t_s))
            else:
                return cv.resize(img_set['tile'], (t_s, t_s))


def random_binary(ratio):
    val = np.random.uniform(low=0, high=1, size=1)[0]
    if val > ratio:
        return False
    else:
        return True


def idx_possible(h, w, r, c):
    return not(r >= h or r < 0 or c >= w or c < 0)


def click(event, x, y, flag, param):
    global current_x
    global current_y
    global left_click

    if event == cv.EVENT_LBUTTONDOWN:
        current_y = int(y/40)
        current_x = int(x/40)
        left_click = True
    if event == cv.EVENT_RBUTTONDOWN:
        current_y = int(y/40)
        current_x = int(x/40)
        left_click = False


(current_y, current_x) = (-1, -1)
left_click = True

img_dict = {
    1:cv.imread('./image/one.png', cv.IMREAD_GRAYSCALE), 
    2:cv.imread('./image/two.png', cv.IMREAD_GRAYSCALE),
    3:cv.imread('./image/three.png', cv.IMREAD_GRAYSCALE),
    4:cv.imread('./image/four.png', cv.IMREAD_GRAYSCALE),
    5:cv.imread('./image/five.png', cv.IMREAD_GRAYSCALE),
    6:cv.imread('./image/six.png', cv.IMREAD_GRAYSCALE),
    7:cv.imread('./image/seven.png', cv.IMREAD_GRAYSCALE),
    8:cv.imread('./image/eight.png', cv.IMREAD_GRAYSCALE),
    0:cv.imread('./image/zero.png', cv.IMREAD_GRAYSCALE),
    'tile':cv.imread('./image/tile.png', cv.IMREAD_GRAYSCALE),
    'mine':cv.imread('./image/mine.png', cv.IMREAD_GRAYSCALE),
    'flag':cv.imread('./image/flag.png', cv.IMREAD_GRAYSCALE)
}


game = MineSweeper()
cv.namedWindow('MineSweeper')
cv.setMouseCallback('MineSweeper', click)

game.game_start()





