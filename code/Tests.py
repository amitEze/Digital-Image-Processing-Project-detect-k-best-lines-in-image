import numpy as np
import cv2
from Methods import draw_best_k_lines


# Tests for draw_best_k_lines
def test():
    srcs = [f'Examples\Example{i}.jpg' for i in range(1,5)]
    # path = 'C:\Users\ezer6\Desktop\Projects\DIP Project\updated\Outputs'
    for i,src in enumerate(srcs):
        img = cv2.imread(src)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        img = draw_best_k_lines(img,T1=100, T2=200, k=7, color=(0,0,255), window_size=2)
        
        canny = cv2.Canny(img, 100, 200, apertureSize=3)
        # os.listdir(path)
        cv2.imwrite(f'OutPut Example{i+1}.jpg',img)
        cv2.imwrite(f'Canny Example{i+1}.jpg',canny)
        print(f'Example{i+1}')

test()