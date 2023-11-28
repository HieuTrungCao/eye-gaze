import cv2
import pyautogui
import numpy as np
import pyautogui
from pynput.keyboard import Controller
from keys import Key
from gaze_tracking import GazeTracking
import time
import keyboard

gaze = GazeTracking('model/shape_predictor_68_face_landmarks.dat')
screen_width, screen_height = pyautogui.size()

def getMousPos(event , x, y, flags, param):
    global posX, posY
    if event == cv2.EVENT_MOUSEMOVE:
        posX, posY = x, y
    
key_board = np.array([["n", "h", "t", "i", 'c'], 
                      ["g", "a", "d", "m",'u'], 
                      ["ô", "à", "o", "y", 'l'], 
                      ["r", "k", "v", "b", 'ư'], 
                      ["s", "ó", "Đổi", "Space", 'Enter']])

keys = {
    "a" : ["a", "á", "à", "ả", "ã", "ạ", "â", "ấ", "ầ", "ẩ", "ẫ", "ậ", "ă", "ắ", "ằ", "ẳ", "ẵ", "ặ"],
    "e" : ["e", "é", "è", "ẻ", "ẽ", "ẹ", "ê", "ế", "ề", "ể", "ễ", "ệ"],
    "y" : ["y", "ý", "ỳ", "ỷ", "ỹ", "ỵ"],
    "i" : ["i", "í", "ì", "ỉ", "ĩ", "ị"],
    "o" : ["o", "ó", "ò", "ỏ", "õ", "ọ", "ô", "ố", "ồ", "ổ", "ỗ", "ộ", "ơ", "ớ", "ờ", "ở", "ỡ", "ợ"],
    "u" : ["u", "ú", "ù", "ủ", "ũ", "ụ", "ư", "ứ", "ừ", "ử", "ữ", "ự"]      
}
n_rows = key_board.shape[0] + 1
d_rows = 10
n_cols = key_board.shape[1]
d_cols = 10

w_key = int((screen_width - (n_cols - 1) * d_cols) / n_cols)
h_key = int((screen_height - (n_rows - 1) * d_rows) / n_rows)

# x_start = int((screen_width - w_key*n_cols - d_cols*(n_cols - 1))/2)
# y_start = int((screen_height - h_key*n_rows - d_rows*(n_rows - 1))/2)
x_start = 0
y_start = 0
       
keys = []

textBox = Key(x_start, y_start, w_key * n_cols + d_cols * (n_cols - 1), h_key, '')

keys.append(textBox)

for y, row in enumerate(key_board, 1):

    x = 0
    while x < len(row):
        count  = 1
        
        for i in range(x + 1, len(row)):
            if row[x] == row[i]:
                x += 1
                count += 1
                continue

        keys.append(Key(x_start + (x - count + 1) * (w_key + d_cols), y_start + y * (h_key + d_rows), w_key * count + d_cols * (count - 1), h_key, row[x]))
        
        x += 1
        
cap = cv2.VideoCapture(0)

posX, posY = 0, 1
previousClick = 0
init = 0
temp_key = keys[1]
prev = 0
# keyboard = Controller()
screen = np.ones((screen_height, screen_width, 3), np.uint8)*255

for k in keys:
    screen = k.drawKey(screen,(255,255,255), (0, 0, 0), alpha=0.5)
        
while True:
    _, frame = cap.read()

    textBox.drawKey(screen, (255,255,255), (0,0,0), 0.3)
    # gaze.refresh(frame)
    
    if keyboard.is_pressed("a") and posY > 1:
        print('Left!')
        if time.time() - previousClick > 0.5:
            posY -= 1
            previousClick = time.time()
    elif  keyboard.is_pressed("d") and posY < n_cols:
        print('Right!')
        if time.time() - previousClick > 0.5:
            posY += 1
            previousClick = time.time()
    elif keyboard.is_pressed("w") and posX > 0:
        print('Up!')
        if time.time() - previousClick > 0.5:
            posX -= 1
            previousClick = time.time()
    elif keyboard.is_pressed("s") and posX < n_rows:
        print('Down!')
        if time.time() - previousClick > 0.5:
            posX += 1
            previousClick = time.time()
            
    # for k in keys:
    #     alpha = 0.5
    #     if k.text == key_board[posX, posY-1]:
    #         alpha = 0.8
    #         if k.isOver(posX, posY):
    #             clickTime = time.time()
    #             if clickTime - previousClick > 2:                          
    #                 if k.text == '<--':
    #                     textBox.text = textBox.text[:-1]
    #                 elif k.text == 'clr':
    #                     textBox.text = ''
    #                 elif len(textBox.text) < 30:
    #                     if k.text == 'Space':
    #                         textBox.text += " "
    #                     else:
    #                         textBox.text += k.text
    #                 previousClick = clickTime

    #     screen = k.drawKey(screen,(255,255,255), (0, 0, 0), alpha=alpha)
    #     alpha = 0.5
    cur = time.time()
    if cur - init > 1:
        key = keys[posX * n_cols + posY]
        if temp_key != key:
            screen = np.ones((screen_height, screen_width, 3), np.uint8)*255
            for k in keys:
                if k != key:
                    screen = k.drawKey(screen,(255,255,255), (0, 0, 0), alpha=0.5)
            temp_key = key         
        
        if key.alpha != 0.8:
            screen = key.drawKey(screen, (255,255,255), (0, 0, 0), alpha=0.8)
        init = cur

        if key.isOver(posX, posY):
            curr = time.time()
            if curr - prev > 2:                          
                if key.text == '<--':
                    textBox.text = textBox.text[:-1]
                elif key.text == 'clr':
                    textBox.text = ''
                elif len(textBox.text) < 30:
                    if key.text == 'Space':
                        textBox.text += " "
                    else:
                        textBox.text += key.text
                prev = curr
    
    cv2.imshow('keyboard', screen)

    pressedKey = cv2.waitKey(1)
    if pressedKey == ord('q'):
        break
    
cv2.destroyAllWindows()         