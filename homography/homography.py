
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv



L = cv.imread('left.png', cv.IMREAD_GRAYSCALE)
R = cv.imread('right.png', cv.IMREAD_GRAYSCALE)

def NMS(a):
    [height, width] = a.shape

    win_size = 7
    offset = int(win_size/2)
    res = []


    for y in range(offset, height - offset):
        for x in range(offset, width - offset):
            if a[y, x] != 0:
                window = a[y - offset:y + offset + 1, x - offset:x + offset + 1]
                if a[y, x] == np.max(window):
                    res.append([y, x])
    
    return res


def harris_corner(img):

    [height, width] = img.shape

    Ix = cv.Sobel(img, cv.CV_8U, 1, 0, ksize = 3)
    Iy = cv.Sobel(img, cv.CV_8U, 0, 1, ksize = 3)

    Ix = np.multiply(Ix, 1/255)
    Iy = np.multiply(Iy, 1/255)

    IxIx = np.multiply(Ix, Ix)
    IxIy = np.multiply(Ix, Iy)
    IyIy = np.multiply(Iy, Iy)
    
    cornermap = np.zeros(img.shape)

    win_size = 3
    offset = int(win_size/2)

    for y in range(offset, height - offset):
        for x in range(offset, width - offset):
            win_IxIx = IxIx[y - offset:y + offset + 1, x - offset:x + offset + 1]
            win_IxIy = IxIy[y - offset:y + offset + 1, x - offset:x + offset + 1]
            win_IyIy = IyIy[y - offset:y + offset + 1, x - offset:x + offset + 1]

            MIxIx = np.sum(win_IxIx)
            MIxIy = np.sum(win_IxIy)
            MIyIy = np.sum(win_IyIy)

            A = np.array([[MIxIx, MIxIy], [MIxIy, MIyIy]])
            det = np.linalg.det(A)
            trace = MIxIx + MIyIy

            k = 0.04
            R = det - np.multiply(k, np.power(trace, 2))

            if R > 0.1:
                cornermap[y,x] = R
    
    feature_list = NMS(cornermap)

    return feature_list

print(harris_corner(L))





