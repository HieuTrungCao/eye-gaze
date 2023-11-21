import cv2
import pyautogui
import numpy as np
import pyautogui

from keys import Key

screen_width, screen_height = pyautogui.size()

frame = np.ones((screen_height, screen_width, 3), np.uint8)*255  # creating a white background  

# cv2.namedWindow('image', cv2.WINDOW_NORMAL)
# cv2.setWindowProperty('image', cv2.WND_PROP_FULLSCREEN, cv2.WND_PROP_FULLSCREEN)

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

text = "text"

keys.append(Key(x_start, y_start, w_key * n_cols + d_cols * (n_cols - 1), h_key, text))

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
    frame = key.drawKey(frame, text_color=(0,0,0), bg_color=(255,255,255),alpha=0.5, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, thickness=2)

# cv2.moveWindow('keyboard', 0, 0)
cv2.imshow('keyboard', frame)
key = cv2.waitKey(0)
# Destroy all windows
cv2.destroyAllWindows()         