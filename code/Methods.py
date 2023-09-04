import cv2
import numpy as np
import os

def draw_lines_by_points(img, lines, color=(0,255,0), thickness=2):
    for line in lines:
        cv2.line(img, line[0], line[1], color, thickness)
    return img


def sliding_window(canny, y, x, window_size):
    # return True if (y,x) neighbor is on line
    # return weight according to distance between spotted pixel to (y,x)
    bool, weight = False, 0
    rows, cols = canny.shape
    for i in range(y-window_size, y+window_size+1):
        for j in range(x-window_size, x+window_size+1):
            if i>-1 and i<rows and j>-1 and j<cols:
                if canny[i, j] == 255:
                    bool = True
                    dx = abs(x-j)
                    dy = abs(y-i)
                    weight = max(weight, window_size -(dx+dy))
    return bool, weight

def bresenham(x0, y0, x1, y1):
    """Yield integer coordinates on the line from (x0, y0) to (x1, y1).
    Input coordinates should be integers.
    The result will contain both the start and the end point.
    """
    dx = x1 - x0
    dy = y1 - y0

    xsign = 1 if dx > 0 else -1
    ysign = 1 if dy > 0 else -1

    dx = abs(dx)
    dy = abs(dy)

    if dx > dy:
        xx, xy, yx, yy = xsign, 0, 0, ysign
    else:
        dx, dy = dy, dx
        xx, xy, yx, yy = 0, ysign, xsign, 0

    D = 2*dy - dx
    y = 0

    for x in range(dx + 1):
        yield x0 + x*xx + y*yx, y0 + x*xy + y*yy
        if D >= 0:
            y += 1
            D -= 2*dx
        D += 2*dy
        
def scan_line_using_bresenham(canny,line,window_size=2):
    rho, theta = line[:2]
    rows, cols = canny.shape
    max_line = None
    max_count = 0
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
    point_on_line = list(bresenham(x1,y1,x2,y2))
    i = 0
    while i < len(point_on_line):
        pt = point_on_line[i]
        x, y = pt[0], pt[1]
        on_line, weight = sliding_window(canny ,y ,x, window_size)
        cur_line_weight = 0
        count = 0
        while on_line and i < len(point_on_line):
                pt = point_on_line[i]
                x, y = pt[0], pt[1]
                cur_line_weight += weight
                # count==0 means new sequence of a line
                if count == 0:
                    point1 = (x,y)
                count += 1
                point2 = (x,y)
                i +=1
                on_line, weight = sliding_window(canny ,y ,x, window_size)
        # longest line untill now
        if max_count < count:
            max_count = count
            main_line = [point1, point2, cur_line_weight, count]
        i +=1
    
    return main_line

def draw_best_k_lines(img, T1=100, T2=200, k=7, color=(0,255,0), window_size=2):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(canny, 1, np.pi/180, 200)
    lines = np.array(list(map(lambda l: l[0],lines)))
    
    canny = cv2.Canny(gray, T1, T2, apertureSize=3)
    lines = np.array(list(map(lambda l: scan_line_using_bresenham(canny,l, window_size),lines)))
    sorted_lines = sorted(lines, key=lambda l: (l[3], l[2]), reverse=True)
    sorted_lines = np.array(list(map(lambda l: [l[0],l[1]], sorted_lines)))
    best_ks = sorted_lines[:k]
    img = draw_lines_by_points(img,best_ks, color)
    return img

def draw_all_lines(img, T1=50, T2=150, color=(0,255,0)):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(canny, 1, np.pi/180, 200)
    lines = np.array(list(map(lambda l: l[0],lines)))
    
    canny = cv2.Canny(gray, T1, T2, apertureSize=3)
    vertical_lines = np.array(list(map(lambda l: scan_line_using_bresenham(canny,l),lines)))
    sorted_lines = sorted(vertical_lines, key=lambda l: (l[2], l[3]), reverse=True)
    sorted_lines = np.array(list(map(lambda l: [l[0],l[1]], sorted_lines)))
    
    img = draw_lines_by_points(img,sorted_lines, color)
    return img

