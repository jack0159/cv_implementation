import numpy as np
import cv2 as cv

class game:
    # Initialization (Level Select & Game Board Create)
    def __init__(self):
        self.__level = int(input("Select Level : "))
        self.m_board = board(self.__level)

class board:

    # Initialization (Raw Board Create)
    def __init__(self, level):

        global raw_height
        global raw_width

        # Set Raw Board's Size
        raw_width = int(level*6*1.2) 
        raw_height = int(level*6*0.8)

        # Mining
        self.raw_board = np.random.choice([0, 1], size = (raw_height, raw_width), p = [0.7, 0.3])

        # Padding for Compute
        self.raw_board = np.pad(self.raw_board, (1, 1))

        # Number of Mine
        self.mine_left = sum(sum(self.raw_board))


        # Computing Raw Board
        win_size = 3
        offset = int(win_size/2)
        temp = np.zeros((raw_height, raw_width))

        for r in range(offset, raw_height - offset + 2):
            for c in range(offset, raw_width - offset + 2):
                if self.raw_board[r, c] == 0:
                    window = self.raw_board[r - offset:r + offset + 1, c - offset:c + offset + 1]
                    temp[r - offset, c - offset] = np.sum(window)
                else:
                    temp[r - offset, c - offset] = -1

        self.raw_board = temp

        # Create Opened Map
        self.opened = np.zeros(self.raw_board.shape)

        # Create Score Board
        self.score_board = np.zeros((100,150))

    # Return image of number
    def __num2img(self, n):
        if n == -1:
            return mine
        else:
            return num_dict[n]

    # Create Display Board
    def raw2display(self):

        global display_height
        global display_width

        display_height = raw_height*cell_size
        display_width = raw_width*cell_size

        display = np.zeros((display_height, display_width))

        for i in range(raw_height):
            for j in range(raw_width):
                pos = (int(j*cell_size + (cell_size/2)), int(i*cell_size + (cell_size/2)))
                display[i*cell_size:(i + 1)*cell_size, j*cell_size:(j + 1)*cell_size] = cv.resize(self.__num2img(self.raw_board[i, j]), (cell_size, cell_size))
        
        return display

    # Digging
    def dig(self, idx):
        (r, c) = idx
        if self.opened[r, c] != 1:
            self.opened[r, c] = 1
        else:
            return

        if self.raw_board[r, c] == 0:
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if idx_possible(raw_height, raw_width, r + i, c + j):
                        self.dig((r + i, c + j))

    # Flag
    def flag(self, idx):
        (r, c) = idx
        self.opened[r, c] = -1
        self.mine_left = self.mine_left - 1

    # Flag Remove
    def flagrm(self, idx):
        (r, c) = idx
        self.opened[r, c] = 0
        self.mine_left = self.mine_left + 1

    # Game
    def gameStart(self):

        # Interface#############################
        print("\nLClick : Open")
        print("RClick : Flag\n")
        print('Answer : ')
        print(self.raw_board) 
        ########################################

        global curR
        curR = -1

        display = self.raw2display()
        concealed = np.zeros((display_height, display_width))
        cur_board = concealed

        mine_cnt = self.mine_left

        while True:

            # Displaying Score Board
            self.score_board = np.zeros((100,150))
            cv.putText(self.score_board, str(self.mine_left) + ' left', (0,100), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
            cv.imshow('Score', self.score_board)
            
            # Click Events
            if curR != -1:
                if cursorType == 0:
                    self.dig((curR, curC))
                elif cursorType == 1:
                    if self.opened[curR, curC] == 0:
                        self.flag((curR, curC))
                    elif self.opened[curR, curC] == -1:
                        self.flagrm((curR, curC))
                curR = -1


            # Display Update
            for r in range(raw_height):
                for c in range(raw_width):

                    if self.opened[r, c] == 1:
                        if self.raw_board[r, c] == -1:
                            print("You Failed")
                            return
                        else:
                            cur_board[r*cell_size:(r + 1)*cell_size, c*cell_size:(c + 1)*cell_size] = display[r*cell_size:(r + 1)*cell_size, c*cell_size:(c + 1)*cell_size]
                    
                    elif self.opened[r, c] == -1:
                        cur_board[r*cell_size:(r + 1)*cell_size, c*cell_size:(c + 1)*cell_size] = cv.resize(flag, (cell_size, cell_size))

                    else:
                        cur_board[r*cell_size:(r + 1)*cell_size, c*cell_size:(c + 1)*cell_size] = np.zeros((cell_size, cell_size))

            for i in range(raw_height):
                for j in range(raw_width):
                    cv.line(cur_board, (j * cell_size, 0), (j * cell_size, raw_height * cell_size - 1), (255, 255, 255))
                    cv.line(cur_board, (0, i * cell_size), (raw_width * cell_size - 1, i * cell_size), (255, 255, 255))

            cv.imshow('board', cur_board)

            # Win Check
            cnt = 0
            for i in range(self.opened.shape[0]):
                for j in range(self.opened.shape[1]):
                    if self.raw_board[i, j] != -1:
                        if self.opened[i, j] == 1:
                            cnt = cnt + 1
            
            if cnt == self.opened.shape[0]*self.opened.shape[1] - mine_cnt:
                print("You Won!!")
                break
            
            # ESC
            if cv.waitKey(1) == 27:
                break

# Search Possibility
def idx_possible(h, w, r, c):
    return not(r >= h or r < 0 or c >= w or c < 0)

# Click Event Function
def click(event, x, y, flag, param):
    global curR
    global curC
    global cursorType

    if event == cv.EVENT_LBUTTONDOWN:
        curR = int(y/40)
        curC = int(x/40)
        cursorType = 0
    if event == cv.EVENT_RBUTTONDOWN:
        curR = int(y/40)
        curC = int(x/40)
        cursorType = 1

# Global Variables
(curR, curC) = (-1, -1)
cursorType = 0
(raw_height, raw_width) = (0 ,0)
(display_height, display_width) = (0,0)
cell_size = 40

# Images
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

# Main
start = game()
cv.namedWindow('board')
cv.setMouseCallback('board', click)

start.m_board.gameStart()
