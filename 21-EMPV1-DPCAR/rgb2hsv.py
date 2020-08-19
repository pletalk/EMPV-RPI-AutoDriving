import cv2
import sys
import numpy as np

'''
RGB를 HSV로 변환하는 프로그램 
@2020-08-18

'''

def split_rgb(arg):
	rgb_list = arg.split(',')
	int_rgb_list = [int(x) for x in rgb_list]

	return int_rgb_list

if __name__ == '__main__':
    rgb_list = np.uint8([[split_rgb(sys.argv[1])]])
    print("RGB=>",rgb_list[0][0])

    hsv = cv2.cvtColor(rgb_list,cv2.COLOR_RGB2HSV)
    print("HSV=>",hsv[0][0])
