import numpy as np
import cv2
from Methods import draw_best_k_lines
import sys

while True:
    
    src = str(input("Enter Image Path :\n"))
    img = cv2.imread(src)
    while img is None:
        print('\nWrong image Path, put the image in same directory of program and print the file name as follows : imagename.jpg')
        src = str(input("Enter Image Path :\n"))
        img = cv2.imread(src)
        
    
    print("\nThe program can operate with different paramaters whereas")
    print("k - number of lines to detect\nT1,T2 - lower and upper Thresholds\nwindow size - how many neighbors for each side of pixel program should check to find an edge")
    mode = str(input("For which parameters the program should operate (Enter number):\n1) no parameters \n2) k \n3) k, T1,T2\n4) k,T1,T2,window size\n"))
    
    if mode == '1':
        img = draw_best_k_lines(img)
        cv2.imshow(f'best 7 lines',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    if mode == '2':
        k = int(input('enter k: '))
        img = draw_best_k_lines(img, k=k)
        cv2.imshow(f'best {k} lines',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    elif mode == '3':
        k = int(input('enter k: '))
        T1 = int(input('enter T1: '))
        T2 = int(input('enter T2: '))
        img = draw_best_k_lines(img, T1, T2, k=k)
        cv2.imshow(f'best {k} lines',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    elif mode == '4':
        k = int(input('enter k: '))
        T1 = int(input('enter T1: '))
        T2 = int(input('enter T2: '))
        window_size = int(input('enter window size: '))
        img = draw_best_k_lines(img, T1, T2, k=k, window_size=window_size)
        cv2.imshow(f'best {k} lines',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    else:
        print('Wrong option')
        


