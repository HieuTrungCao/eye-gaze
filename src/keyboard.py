import cv2
import pyautogui
import numpy as np
import pyautogui
from pynput.keyboard import Controller
from keys import Key
from checkevent import getMousPos

def getMousPos(event , x, y, flags, param):
    global clickedX, clickedY
    global mouseX, mouseY
    if event == cv2.EVENT_LBUTTONUP:
        print(x,y)
        clickedX, clickedY = x, y
    if event == cv2.EVENT_MOUSEMOVE:
    #     print(x,y)
        mouseX, mouseY = x, y

screen_width, screen_height = pyautogui.size()
frame = np.ones((screen_height, screen_width, 3), np.uint8)*255
    
key_board = [["n", "h", "t", "i", 'c'], ["g", "a", "d", "m",'u'], ["ô", "à", "o", "y", 'l'], ["r", "k", "v", "b", 'ư'], ["s", "ó", "Đổi", "Space", 'Enter']]

n_rows = key_board.__len__() + 1
d_rows = 10
n_cols = key_board[0].__len__()
d_cols = 10

w_key = int((screen_width - (n_cols - 1) * d_cols) / n_cols)
h_key = int((screen_height - (n_rows - 1) * d_rows) / n_rows)

x_start = int((screen_width - w_key*n_cols - d_cols*(n_cols - 1))/2)
y_start = int((screen_height - h_key*n_rows - d_rows*(n_rows - 1))/2)
       
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
        
for key in keys:
    key.drawKey(frame, text_color=(0,0,0), bg_color=(255,255,255),alpha=0.5, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, thickness=2)
    
cap = cv2.VideoCapture(0)

clickedX, clickedY = 0, 0
mouseX, mouseY = 0, 0

previousClick = 0

keyboard = Controller()

while True:
    textBox.drawKey(frame, (255,255,255), (0,0,0), 0.3)
    cv2.setMouseCallback('keyboard', getMousPos)
    for k in keys:
        alpha = 0.5
        if k.isOver(mouseX, mouseY):
            alpha = 0.1
            if k.isOver(clickedX, clickedY):                            
                if k.text == '<--':
                    textBox.text = textBox.text[:-1]
                elif k.text == 'clr':
                    textBox.text = ''
                elif len(textBox.text) < 30:
                    if k.text == 'Space':
                        textBox.text += " "
                    else:
                        textBox.text += k.text
                        
            # writing using fingers
            # if (k.isOver(thumbTipX, thumbTipY)):
            #     clickTime = time.time()
            #     if clickTime - previousClick > 0.4:                               
            #         if k.text == '<--':
            #             textBox.text = textBox.text[:-1]
            #         elif k.text == 'clr':
            #             textBox.text = ''
            #         elif len(textBox.text) < 30:
            #             if k.text == 'Space':
            #                 textBox.text += " "
            #             else:
            #                 textBox.text += k.text
            #                 #simulating the press of actuall keyboard
            #                 keyboard.press(k.text)
            #         previousClick = clickTime
        k.drawKey(frame,(255,255,255), (0,0,0), alpha=alpha)
        alpha = 0.5
    clickedX, clickedY = 0, 0 
    
    cv2.imshow('keyboard', frame)
    ## stop the video when 'q' is pressed
    pressedKey = cv2.waitKey(1)
    if pressedKey == ord('q'):
        break
# cv2.moveWindow('keyboard', 0, 0)
# key = cv2.waitKey(0)
cv2.destroyAllWindows()         