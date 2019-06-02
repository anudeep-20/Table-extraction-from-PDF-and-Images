from IPython.display import Image, HTML
import pandas as pd
import numpy as np
import pdb
import cv2
import sys

BUFFER_LENGTH = 10
DEFAULT_PIXEL_COLOR = 255
PAGE_BREAK_HANDLE = '"||page_break||"'
DEFAULT_APERTURE_SIZE = 3

def get_straight_lines(img, aperture_size=3):                                                                                                         
    
    edges = cv2.Canny(img, 50, 150, apertureSize=aperture_size)
    min_line_length = 100                                                                                             
    max_line_gap = 25
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 80, min_line_length,
                            max_line_gap)
    return lines


def get_horizontal_base_line(lines):
    '''Gives vertical coordinate of horizontal base line(aka header line) 
    '''
    horizontal_base_line = 0
    for line in lines:
        for x1, y1, x2, y2 in line:
            if y1 == y2 and (horizontal_base_line == 0 or horizontal_base_line > y1):
                horizontal_base_line = y1 + BUFFER_LENGTH
    return horizontal_base_line

def get_max_stretch(coordinate, stretch_vector):
    if stretch_vector[0] == stretch_vector[1] == 0:
        stretch_vector[0] = stretch_vector[1] = coordinate + BUFFER_LENGTH
    elif coordinate < stretch_vector[0]:
        stretch_vector[0] = coordinate - BUFFER_LENGTH
    elif coordinate > stretch_vector[1]:
        stretch_vector[1] = coordinate + BUFFER_LENGTH
    return stretch_vector

def get_table_limits(img, lines, is_header): 
    '''Get maximum horizontal and vertical line coordinates for bounding box
    '''
    table_limits = {}
    found_horizontal_line = False
    found_vertical_line = False
    vertical_stretch = [0,0]
    horizontal_stretch = [0,0]
    max_horizontal = [0,0,0,0]
    max_vertical = [0,0,0,0]
    horizontal_base_line = 0
    if is_header:
        horizontal_base_line = get_horizontal_base_line(lines)
    vertical_base_line = 0
    if type(lines).__module__ == "numpy":
        for line in lines:
            print(line)
            for x1,y1,x2,y2 in line:
                if x1 == x2:
                    if not found_vertical_line:
                        found_vertical_line = True
                    length = (y1 - y2)
                    if max_vertical[0] <= length:
                        max_vertical[0] = length
                        max_vertical[1] = y1 + BUFFER_LENGTH
                        max_vertical[2] = y2 - BUFFER_LENGTH
                    if (max_vertical[3] == 0 or max_vertical[3] > (x1 - BUFFER_LENGTH)) and (x1 - BUFFER_LENGTH) > vertical_base_line:
                        max_vertical[3] = (x1 - BUFFER_LENGTH)
                    horizontal_stretch = get_max_stretch(x1, horizontal_stretch)
                elif y1 == y2:
                    if not found_horizontal_line:
                        found_horizontal_line = True
                    length = (x2 - x1)
                    if max_horizontal[0] <= length:
                        max_horizontal[0] = length
                        max_horizontal[1] = x1 - BUFFER_LENGTH
                        max_horizontal[2] = x2 + BUFFER_LENGTH
                    if (max_horizontal[3] == 0 or max_horizontal[3] > (y1 - BUFFER_LENGTH)) and (y1 - BUFFER_LENGTH) > horizontal_base_line:
                        max_horizontal[3] = (y1 - BUFFER_LENGTH)
                    if not is_header:
                        vertical_stretch = get_max_stretch(y1, vertical_stretch)
    print('3')
    if max_vertical[2] > max_horizontal[3] and max_horizontal[3] > 0:
        max_vertical[2] = max_horizontal[3]
    if max_horizontal[1] >  max_vertical[3] and max_vertical[3] > 0:
        max_horizontal[1] = max_vertical[3]
    if (not found_vertical_line and found_horizontal_line) or not is_header:
        max_vertical[1:3] = vertical_stretch
    elif not found_horizontal_line and found_vertical_line:
        max_horizontal[1:3] = horizontal_stretch
    table_limits["horizontal"] = {"stretch": horizontal_stretch, "found": found_horizontal_line, "max": max_horizontal}
    table_limits["vertical"] = {"stretch": vertical_stretch, "found": found_vertical_line, "max": max_vertical}
    return table_limits


def extend_lines_for_table(img, lines, is_header, table_limits):
    ''' 
    Extend straight lines to create table bounds
    '''
    column_coordinates=[]
    for line in lines:
        for x1, y1, x2, y2 in line:
            if x1 == x2: 
                y1 = table_limits["vertical"]["max"][1]
                y2 = table_limits["vertical"]["max"][2]
                if(x1 not in column_coordinates):
                    column_coordinates.append(x1)
            elif y1 == y2: 
                x1 = table_limits["horizontal"]["max"][1]
                x2 = table_limits["horizontal"]["max"][2]
    return column_coordinates



def get_col_borders(filename):
    print(filename)
    lines = get_straight_lines(cv2.imread(filename,0))
    print('lines', lines)
    table_limits = get_table_limits(cv2.imread(filename,0), lines, False)
    column_coordinates = extend_lines_for_table(cv2.imread(filename,0),lines,False,table_limits)
    print('1')
    column_coordinates.sort()
    print(column_coordinates)
    return 1
        
    
if __name__ == '__main__':
    get_col_borders(sys.argv[1])