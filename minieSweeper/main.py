import numpy as np
import cv2 as cv

class game:
    def __init__(self):
        self.__level = int(input("Select Level : "))
        self.m_board = board(self.__level)
    
class board:

    def __init__(self, level):

        width = int(level*6*1.2)
        height = int(level*6*0.8)

        self.raw_board = np.random.choice([0, 1], size = (height, width), p = [0.7, 0.3])
        self.raw_board = np.pad(self.raw_board, (1, 1))

        self.mineCnt = sum(sum(self.raw_board))

        win_size = 3
        offset = int(win_size/2)
        temp = np.zeros((height, width))

        for r in range(offset, height - offset + 2):
            for c in range(offset, width - offset + 2):
                if self.raw_board[r, c] == 0:
                    window = self.raw_board[r - offset:r + offset + 1, c - offset:c + offset + 1]
                    temp[r - offset, c - offset] = np.sum(window)
                else:
                    temp[r - offset, c - offset] = -1
        self.raw_board = temp

        self.opened = np.zeros(self.raw_board.shape)

        self.score_board = np.zeros((100,150))

    def raw2real(self):
        [height, width] = self.raw_board.shape

        self.cell_size = 40
        real = np.zeros((height*self.cell_size, width*self.cell_size))
        for i in range(height):
            for j in range(width):
                pos = (int(j*self.cell_size + (self.cell_size/2)), int(i*self.cell_size + (self.cell_size/2)))
                if self.raw_board[i, j] != -1:
                    if self.raw_board[i, j] == 1:
                        real[i*self.cell_size:(i + 1)*self.cell_size, j*self.cell_size:(j + 1)*self.cell_size] = cv.resize(one, (self.cell_size, self.cell_size))
                    elif self.raw_board[i, j] == 2:
                        real[i*self.cell_size:(i + 1)*self.cell_size, j*self.cell_size:(j + 1)*self.cell_size] = cv.resize(two, (self.cell_size, self.cell_size))
                    elif self.raw_board[i, j] == 3:
                        real[i*self.cell_size:(i + 1)*self.cell_size, j*self.cell_size:(j + 1)*self.cell_size] = cv.resize(three, (self.cell_size, self.cell_size))
                    elif self.raw_board[i, j] == 4:
                        real[i*self.cell_size:(i + 1)*self.cell_size, j*self.cell_size:(j + 1)*self.cell_size] = cv.resize(four, (self.cell_size, self.cell_size))
                    elif self.raw_board[i, j] == 5:
                        real[i*self.cell_size:(i + 1)*self.cell_size, j*self.cell_size:(j + 1)*self.cell_size] = cv.resize(five, (self.cell_size, self.cell_size))
                    elif self.raw_board[i, j] == 6:
                        real[i*self.cell_size:(i + 1)*self.cell_size, j*self.cell_size:(j + 1)*self.cell_size] = cv.resize(six, (self.cell_size, self.cell_size))
                    elif self.raw_board[i, j] == 7:
                        real[i*self.cell_size:(i + 1)*self.cell_size, j*self.cell_size:(j + 1)*self.cell_size] = cv.resize(seven, (self.cell_size, self.cell_size))
                    elif self.raw_board[i, j] == 8:
                        real[i*self.cell_size:(i + 1)*self.cell_size, j*self.cell_size:(j + 1)*self.cell_size] = cv.resize(eight, (self.cell_size, self.cell_size))
                    elif self.raw_board[i, j] == 0:
                        real[i*self.cell_size:(i + 1)*self.cell_size, j*self.cell_size:(j + 1)*self.cell_size] = cv.resize(zero, (self.cell_size, self.cell_size))
                else:
                    real[i*self.cell_size:(i + 1)*self.cell_size, j*self.cell_size:(j + 1)*self.cell_size] = cv.resize(mine, (self.cell_size, self.cell_size))
        
        return real

    def dig(self, idx):
        [h, w] = self.raw_board.shape
        [r, c] = idx
        if self.opened[r, c] == 0:
            self.opened[r, c] = 1
        if self.raw_board[r, c] == 0:
            if idx_possible([h, w], [r + 1, c]):
                    if self.opened[r + 1, c] == 0:
                        self.dig([r + 1, c])
            if idx_possible([h, w], [r , c + 1]):
                    if self.opened[r, c + 1] == 0:
                        self.dig([r, c + 1])
            if idx_possible([h, w], [r + 1, c + 1]):
                    if self.opened[r + 1, c + 1] == 0:
                        self.dig([r + 1, c + 1])
            if idx_possible([h, w], [r - 1, c]):
                    if self.opened[r - 1, c] == 0:
                        self.dig([r - 1, c])
            if idx_possible([h, w], [r, c - 1]):
                    if self.opened[r, c - 1] == 0:
                        self.dig([r, c - 1])
            if idx_possible([h, w], [r - 1, c - 1]):
                    if self.opened[r - 1, c - 1] == 0:
                        self.dig([r - 1, c - 1])
            if idx_possible([h, w], [r + 1, c - 1]):
                    if self.opened[r + 1, c - 1] == 0:
                        self.dig([r + 1, c - 1])
            if idx_possible([h, w], [r - 1, c + 1]):
                    if self.opened[r - 1, c + 1] == 0:
                        self.dig([r - 1, c + 1])
        return

    def flag(self, idx):
        [r, c] = idx
        if clk < 8:
            self.opened[r, c] = -1
            self.score_board = np.zeros((100,200))
            self.mineCnt = self.mineCnt - 1
        return

    def flagrm(self, idx):
        [r, c] = idx
        if clk < 8:
            self.opened[r, c] = 0
            self.score_board = np.zeros((100,200))
            self.mineCnt = self.mineCnt + 1
        return


    def display(self):


        global clk

        print("\nLClick : Open")
        print("RClick : Flag\n")

        print('Answer : ')
        print(self.raw_board) 
        

        init_mine_cnt = self.mineCnt
        [height, width] = self.raw2real().shape
        
        concealed = np.zeros((height, width))
        cur_board = concealed
        opened_idx_list = []

        while True:
            
            cv.putText(self.score_board, str(self.mineCnt) + ' left', (0,100), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
            cv.imshow('Score', self.score_board)


            if curR != -1:
                if cursorType == 0:
                    self.dig([curR, curC])
                elif cursorType == 1:
                    if self.opened[curR, curC] == 0:
                        self.flag([curR, curC])
                    elif self.opened[curR, curC] == -1:
                        self.flagrm([curR, curC])

            for r in range(self.opened.shape[0]):
                for c in range(self.opened.shape[1]):

                    if self.opened[r, c] == 1:
                        if self.raw_board[r, c] == -1:
                            print("You Failed")
                            return

                        else:
                            cur_board[r*self.cell_size:(r + 1)*self.cell_size, c*self.cell_size:(c + 1)*self.cell_size] = self.raw2real()[r*self.cell_size:(r + 1)*self.cell_size, c*self.cell_size:(c + 1)*self.cell_size]
                    
                    elif self.opened[r, c] == -1:
                        cur_board[r*self.cell_size:(r + 1)*self.cell_size, c*self.cell_size:(c + 1)*self.cell_size] = cv.resize(flag, (self.cell_size, self.cell_size))

                    else:
                        cur_board[r*self.cell_size:(r + 1)*self.cell_size, c*self.cell_size:(c + 1)*self.cell_size] = np.zeros((self.cell_size, self.cell_size))

            for i in range(self.raw_board.shape[0]):
                for j in range(self.raw_board.shape[1]):
                    cv.line(cur_board, (j * self.cell_size, 0), (j * self.cell_size, height - 1), (255, 255, 255))
                    cv.line(cur_board, (0, i * self.cell_size), (width - 1, i * self.cell_size), (255, 255, 255))

            cv.imshow('board', cur_board)

            cnt = 0
            for i in range(self.opened.shape[0]):
                for j in range(self.opened.shape[1]):
                    if self.raw_board[i, j] != -1:
                        if self.opened[i, j] == 1:
                            cnt = cnt + 1
            
            if cnt == self.opened.shape[0]*self.opened.shape[1] - init_mine_cnt:
                print("You Won!!")
                break
                    
                    

            if cv.waitKey(1) == 27:
                break

            clk = clk + 1

def idx_possible(imgsize, idx):
    [h, w] = imgsize
    [r, c] = idx
    if r >= h:
        return False
    elif r < 0:
        return False
    elif c >= w:
        return False
    elif c < 0:
        return False
    else:
        return True


def click(event, x, y, flag, param):
    global curR
    global curC
    global cursorType   
    global clk

    if event == cv.EVENT_LBUTTONDOWN:
        curR = int(y/40)
        curC = int(x/40)
        cursorType = 0
        clk = 0
    if event == cv.EVENT_RBUTTONDOWN:
        curR = int(y/40)
        curC = int(x/40)
        cursorType = 1
        clk = 0


[curR, curC] = [-1, -1]
cursorType = 0
clk = 1

one = cv.imread('./image/one.png', cv.IMREAD_GRAYSCALE)
two = cv.imread('./image/two.png', cv.IMREAD_GRAYSCALE)
three = cv.imread('./image/three.png', cv.IMREAD_GRAYSCALE)
four = cv.imread('./image/four.png', cv.IMREAD_GRAYSCALE)
five = cv.imread('./image/five.png', cv.IMREAD_GRAYSCALE)
six = cv.imread('./image/six.png', cv.IMREAD_GRAYSCALE)
seven = cv.imread('./image/seven.png', cv.IMREAD_GRAYSCALE)
eight = cv.imread('./image/eight.png', cv.IMREAD_GRAYSCALE)
zero = cv.imread('./image/zero.png', cv.IMREAD_GRAYSCALE)
mine = cv.imread('./image/mine.png', cv.IMREAD_GRAYSCALE)
flag = cv.imread('./image/flag.png', cv.IMREAD_GRAYSCALE)

start = game()

cv.namedWindow('board')
cv.setMouseCallback('board', click)

start.m_board.display()
