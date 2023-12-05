import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image

class Key():

    def __init__(self,x,y,w,h,text,alpha=0.5):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text=text
        self.text_size = 60
        self.font = ImageFont.truetype("font\\arial.ttf", self.text_size)
        self.alpha = alpha
        
    def drawKey(self, img, text_color=(0,0,0), bg_color=(0,0,0),alpha=0.5, fontFace=0, fontScale=0.8, thickness=2):
        
        img = np.array(img)
        #draw the box
        bg_rec = img[self.y : self.y + self.h, self.x : self.x + self.w]
        white_rect = np.ones(bg_rec.shape, dtype=np.uint8) #* 25
        white_rect[:] = bg_color
        # res = cv2.addWeighted(bg_rec, alpha, white_rect, 1-alpha, 1.0)
        
        # Putting the image back to its position
        img[self.y : self.y + self.h, self.x : self.x + self.w] = white_rect

        #put the letter
        # tetx_size = cv2.getTextSize(self.text, fontFace, fontScale, thickness)
        text_size = [[self.text_size, self.text_size]]
        text_pos = (int(self.x + self.w/2 - text_size[0][0]*len(self.text)/2), int(self.y + self.h/2 - text_size[0][1]/2))
        
        pill_img = Image.fromarray(img)
        draw = ImageDraw.Draw(pill_img)
        draw.text(text_pos, self.text, "black", font=self.font)
        img = np.asarray(pill_img)
        # cv2.putText(img, self.text,text_pos, fontFace, fontScale ,text_color, thickness)
        cv2.rectangle(img, (self.x, self.y), (self.x + self.w, self.y + self.h), (0,0,0), 2)        
        # cv2.imshow("key", img)
        return img

    def isOver(self,x,y):
        # if (self.x + self.w > x > self.x) and (self.y + self.h> y >self.y):
        #     return True
        # return False
        if (self.x + self.w == (x+1) * self.w + x * 10) and (self.y + self.h == (y+1) * self.h + y * 10):
            return True
        return False
    