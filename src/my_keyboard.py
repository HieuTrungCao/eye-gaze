import cv2
import pyautogui
import numpy as np
import pyautogui
from pynput.keyboard import Controller
from keys import Key
from text2speech import Speak
import time
import keyboard
from detect_coordinate import Coordinate

screen_width, screen_height = pyautogui.size()
    
key_board_1 = np.array([["Xóa", "o", "y", "l", 'r'], 
                      ["d", "h", "t", "i",'k'], 
                      ["p", "m", "n", "c", 'v'], 
                      ["e", "đ", "a", "g", 'b'], 
                      ["s", "u", "Cách", "Nói", 'Đổi']])
key_board_2 = np.array([["Xóa", "g", "đ", "m", 'l'], 
                      ["c", "i", "a", "u",'r'], 
                      ["t", "q", "x", "o", 'k'], 
                      ["h", "n", "e", "y", 'v'], 
                      ["s", "b", "Cách", "Nói", 'Đổi']])
extend_keyboad = {
    "a":  np.array([["", "", "", "", ''], 
                    ["ặ", "à", "á", "ấ",'ẩ'], 
                    ["ằ", "ã", "a", "ả", 'ẳ'], 
                    ["ẫ", "ậ", "ạ", "â", 'ẵ'], 
                    ["", "ắ", "ầ", "ă", '']]),
    "e":  np.array([["", "", "", "", ''], 
                    ["", "ế", "ê", "ệ",''], 
                    ["", "ẹ", "e", "ể", ''], 
                    ["", "é", "ẽ", "ề", ''], 
                    ["", "è", "ễ", "ẻ", '']]),
    "y":  np.array([["", "", "", "", ''], 
                    ["", "", "ỹ", "",''], 
                    ["", "ý", "y", "ỳ", ''], 
                    ["", "", "ỷ", "ỵ", ''], 
                    ["", "", "", "", '']]),
    "i":  np.array([["", "", "", "", ''], 
                    ["", "", "ị", "",''], 
                    ["", "ì", "i", "í", ''], 
                    ["", "", "ĩ", "ỉ", ''], 
                    ["", "", "", "", '']]),
    "o":  np.array([["", "", "", "", ''], 
                    ["õ", "o", "ó", "ố",'ỡ'], 
                    ["ồ", "ơ", "ô", "ờ", 'ỗ'], 
                    ["ọ", "ợ", "ộ", "ớ", 'ỏ'], 
                    ["", "ở", "ò", "ổ", '']]),
    "u":  np.array([["", "", "", "", ''], 
                    ["", "ư", "ú", "ủ",''], 
                    ["", "ụ", "u", "ứ", ''], 
                    ["", "ự", "ừ", "ữ", ''], 
                    ["", "ũ", "ù", "ử", '']]),
}

n_rows = key_board_1.shape[0] + 1
d_rows = 10
n_cols = key_board_1.shape[1]
d_cols = 10

w_key = int((screen_width - (n_cols - 1) * d_cols) / n_cols)
h_key = int((screen_height - (n_rows - 1) * d_rows) / n_rows)

# x_start = int((screen_width - w_key*n_cols - d_cols*(n_cols - 1))/2)
# y_start = int((screen_height - h_key*n_rows - d_rows*(n_rows - 1))/2)
x_start = 0
y_start = 0
       
textBox = Key(x_start, y_start, w_key * n_cols + d_cols * (n_cols - 1), h_key, '')

def set_key_board(key_board):
    keys = []
    keys.append(textBox)

    for y, row in enumerate(key_board, 1):

        x = 0
        while x < len(row):
            count  = 1
            
            for i in range(x + 1, len(row)):
                if row[x] == row[i] and row[x] != '':
                    x += 1
                    count += 1
                    continue
            
            keys.append(Key(x_start + (x - count + 1) * (w_key + d_cols), y_start + y * (h_key + d_rows), w_key * count + d_cols * (count - 1), h_key, row[x]))
            
            x += 1
    return keys

keys_1 = set_key_board(key_board_1)    
keys_2 = set_key_board(key_board_2)    
keys_extend = {
    "a": set_key_board(extend_keyboad["a"]),
    "e": set_key_board(extend_keyboad["e"]),
    "y": set_key_board(extend_keyboad["y"]),
    "i": set_key_board(extend_keyboad["i"]),
    "o": set_key_board(extend_keyboad["o"]),
    "u": set_key_board(extend_keyboad["u"])
}  

cap = cv2.VideoCapture(0)
prev_posX, prev_posY = 2, 3
posX, posY = 2, 3
previousClick = 0
keys = keys_1
temp_key = keys[1]
key = keys[2 * n_cols + posY]
prev = time.time()

screen = np.ones((screen_height, screen_width, 3), np.uint8)*255

cur = time.time()  

step = 1
is_one = True
is_extend = False
choose_time = 1.8
speaker = Speak()

codinate = Coordinate(screen_width, screen_height)
while True:
    _, frame = cap.read()

    textBox.drawKey(screen, (255,255,255), (0,0,0), 0.3)
    
    ratio_time = 0.3
    
    if keyboard.is_pressed("a") and posY > 1:
        print('Left!')
        if time.time() - previousClick > ratio_time:
            posY -= 1
            previousClick = time.time()
            prev = time.time()
    elif  keyboard.is_pressed("d") and posY < n_cols:
        print('Right!')
        if time.time() - previousClick > ratio_time:
            posY += 1
            previousClick = time.time()
            prev = time.time()
    elif keyboard.is_pressed("w") and posX > 0:
        print('Up!')
        if time.time() - previousClick > ratio_time:
            posX -= 1
            previousClick = time.time()
            prev = time.time()
    elif keyboard.is_pressed("s") and posX < n_rows -2:
        print('Down!')
        if time.time() - previousClick > ratio_time:
            posX += 1
            previousClick = time.time()
            prev = time.time()

    x, y = codinate.detect_condinate(frame)
    
    draw = False
    if temp_key.text == key.text:
        curr = time.time()
        if curr - prev > choose_time and step > 1:  
                          
            if key.text == 'Nói':
                speaker.speak(textBox.text)
            elif key.text == 'Xóa':
                textBox.text = ''
            elif key.text == 'Cách':
                textBox.text += " "
            elif key.text == "Đổi":
                if is_one:
                    keys = keys_2
                    is_one = False
                else:
                    keys = keys_1
                    is_one = True
                prev_posX = 2
                posX = 2
                prev_posY = 3
                posY = 3
            elif key.text in keys_extend.keys() and not is_extend:
                keys = keys_extend[key.text]
                is_extend = True
                prev_posX = 2
                posX = 2
                prev_posY = 3
                posY = 3
            elif is_extend:
                if key.text == "":
                    continue 
                textBox.text += key.text
                is_extend = False
                if is_one:
                    keys = keys_1
                else:
                    keys = keys_2

                prev_posX = 2
                posX = 2
                prev_posY = 3
                posY = 3
                
            else:
                textBox.text += key.text
                    
            prev = curr
            draw = True
        textBox.drawKey(screen,(255,255,255), (192, 192, 192), alpha=0.5)
    
    if prev_posX != posX or prev_posY != posY or draw or step == 1:
        step += 1
        key = keys[posX * n_cols + posY]
        if temp_key != key or step == 2 or draw:
            screen = np.ones((screen_height, screen_width, 3), np.uint8)*255
            for i, k in enumerate(keys):
                
                if k != key:
                    screen = k.drawKey(screen,(255,255,255), (227, 227, 227), alpha=0.5)
            temp_key = key         
        
        if key.alpha != 0.8:
            screen = key.drawKey(screen, (255,255,255), (173, 247, 182), alpha=0.8)
        draw = False
        prev_posX = posX
        prev_posY = posY
    cv2.circle(screen, (x, y), 10, (0, 255, 0), 10)
    cv2.imshow('keyboard', screen)

    pressedKey = cv2.waitKey(1)
    if pressedKey == ord('q'):
        break
    
cv2.destroyAllWindows()         