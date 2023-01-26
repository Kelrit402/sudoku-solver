import cv2
import os
from PIL import ImageGrab,Image
from imutils import contours
import numpy as np
import pytesseract
import clipboard

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\\Tesseract-OCR\\tesseract.exe'
grid = [[0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]]
M = 9
cred = (0,0,255)
cgreen = (0,255,0)
cblue = (255,0,0)
cropsize = 1 #percent

#image = cv2.imread('E:/project/python/1111.png')
pil_image = ImageGrab.grabclipboard()
image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

def drawcutline(img):
    global cropsize
    xoffset = int(img.shape[1]/9)
    yoffset = int(img.shape[0]/9)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    img = cv2.rectangle(img, (0,0),(img.shape[1],0+cropsize),cred,-1)
    img = cv2.rectangle(img, (0,0),(0+cropsize,img.shape[0]),cred,-1)
    img = cv2.rectangle(img, (img.shape[1]-cropsize,0),(img.shape[1],img.shape[0]),cred,-1)
    img = cv2.rectangle(img, (0,img.shape[0]-cropsize),(img.shape[1],img.shape[0]),cred,-1)
    for x in range(1,9):
        img = cv2.rectangle(img, (xoffset*x-cropsize,0),(xoffset*x+cropsize,img.shape[0]),cred,-1)
    for y in range(1,9):
        img = cv2.rectangle(img, (0,yoffset*y-cropsize),(img.shape[1],yoffset*y+cropsize),cred,-1)

    cv2.imshow('result', img)
    cv2.waitKey(30)
    print("enter masking size or y")
    input1 = input()
    if input1 != "y":
        cropsize = int(input1)
        drawcutline(image)

def imgbrightness(img, value):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    v-=value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img

def drawfin(img):
    xoffset = int(img.shape[1]/9)
    yoffset = int(img.shape[0]/9)
    cutx = int(5/xoffset*100*5)
    cuty = int(5/yoffset*100*5)
    img = imgbrightness(img, 50)
    img = cv2.rectangle(img, (0,0),(img.shape[1],0+cropsize),cred,-1)
    img = cv2.rectangle(img, (0,0),(0+cropsize,img.shape[0]),cred,-1)
    img = cv2.rectangle(img, (img.shape[1]-cropsize,0),(img.shape[1],img.shape[0]),cred,-1)
    img = cv2.rectangle(img, (0,img.shape[0]-cropsize),(img.shape[1],img.shape[0]),cred,-1)
    for x in range(1,9):
        img = cv2.rectangle(img, (xoffset*x-cropsize,0),(xoffset*x+cropsize,img.shape[0]),cred,-1)
    for y in range(1,9):
        img = cv2.rectangle(img, (0,yoffset*y-cropsize),(img.shape[1],yoffset*y+cropsize),cred,-1)
    for y in range(9):
        for x in range(9):
            img = cv2.putText(img,str(grid[y][x]),((xoffset*x)+cutx,((yoffset)*(y+1))-cuty),cv2.FONT_HERSHEY_SIMPLEX,2,cblue,4,cv2.LINE_AA)
    cv2.imshow('result', img)
    cv2.waitKey(30)

def readimg():
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thres = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,57,5)
    U = 0
    V = 0
    for x in range(9):
        yoffset = int(thres.shape[1]/9)
        xoffset = int(thres.shape[0]/9)
        cutx = int(cropsize/xoffset*100)
        cuty = int(cropsize/yoffset*100)
        imgxcrop = thres[xoffset*x+cutx:xoffset*(x+1)-cutx, 0:thres.shape[0]]
        #cv2.imshow('result', imgxcrop)
        for y in range(9):
            imgyrop = imgxcrop[0:thres.shape[1], yoffset*y+cuty:yoffset*(y+1)-cuty]
            #cv2.imshow('result', imgyrop)
            tnum = pytesseract.image_to_string(imgyrop, lang='eng', config='--psm 10 --oem 3 -c tessedit_char_whitelist=123456789')
            if tnum == '':
                tnum = 0
            else:
                tnum = int(tnum)
            if tnum > 9:
                return False
            #print(tnum)
            grid[V][U] = tnum
            U+=1
            if U >= 9:
                U = 0
                V+=1
                puzzle(grid,True)
            #cv2.waitKey(100)
    return True

def modifymode():
    numi = 0
    for i in grid:
        numu = 0
        numut = "^"
        for u in i:
            linetemp = ""
            print("---modify mode line {}---".format(numi+1))
            for y in range(9):
                linetemp = linetemp + str(grid[numi][y]) + " "
            print(linetemp)
            print(numut)
            numinput = input()
            #print("("+numinput+")")
            if numinput == "s":
                continue
            if numinput == "y":
                return
            if numinput == '':
                numinput = grid[numi][numu]
            else:
                numinput = int(numinput)
            grid[numi][numu] = int(numinput)
            numu+=1
            numut = "  " + numut
        numi+=1

def modifymode2():
    print("enter coord to fix or n")
    ninput = input()
    if ninput == 'n':
        return
    print("enter correct value")
    ninput2 = int(input())
    grid[int(ninput[0])-1][int(ninput[1])-1] = ninput2
    drawfin(image)
    puzzle(grid)
    modifymode2()

def puzzle(a,flush=False):
    returntext = ''
    for i in range(M):
        if i%3==0 and i!=0:
             returntext += '-----------------------\n'
        for j in range(M):
            if j%3==0 and j!=0:
                returntext += '| '
            returntext += str(a[i][j])+' '
        returntext += '\n'
    if flush:
        os.system('cls')
    print(returntext)

#https://www.askpython.com/python/examples/sudoku-solver-in-python
def solve(grid, row, col, num):
    for x in range(9):
        if grid[row][x] == num:
            return False
             
    for x in range(9):
        if grid[x][col] == num:
            return False
 
 
    startRow = row - row % 3
    startCol = col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[i + startRow][j + startCol] == num:
                return False
    return True
 
def Suduko(grid, row, col):
 
    if (row == M - 1 and col == M):
        return True
    if col == M:
        row += 1
        col = 0
    if grid[row][col] > 0:
        return Suduko(grid, row, col + 1)
    for num in range(1, M + 1, 1): 
     
        if solve(grid, row, col, num):
         
            grid[row][col] = num
            #puzzle(grid)
            if Suduko(grid, row, col + 1):
                return True
        grid[row][col] = 0
    return False
 
def dosolver():
    drawcutline(image)
    print("reading..")
    isred = readimg()
    if isred == False:
        print("reading failed!")
        return False
    os.system('cls')
    print("\r====read success====")
    drawfin(image)
    puzzle(grid)
    modifymode2()
    if (Suduko(grid, 0, 0)):
        print("====solve success====")
        puzzle(grid)
        drawfin(image)
        cv2.waitKey()
    else:
        print("====solve failed====")
        puzzle(grid)

dosolver()
