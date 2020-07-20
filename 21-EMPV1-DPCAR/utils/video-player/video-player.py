#!/usr/bin/env python3

'''
$video_player.py 

이미지형태의 주행영상을 입력으로 받아서 뷰잉하는 프로그램 

@2020-07-06 / @ignitespark


Usage:
- avi포맷의 동영상을 입력으로 받아서 플레이입니다
- 이이지 표시창을 사라지게 하려면, 이미지 창이 선택된 상황에서 q를 누르면
  이미지 창이 사라집니다.
- 이미지 창표시를 위해서 GUI환경에서 프로그램을 수행합니다.
  (명령행에서 수행하면, GTK오류가 발생됩니다)
'''

import os,sys,json,argparse
import time
import pprint
import cv2

from docopt import docopt
import numpy as np


#
# cmdargs_parsing : 명령형의 인수를 파싱하는 함수
#
def cmdargs_parsing(parser):
	parser.add_argument('--src', required=True, help='video파일의 경로를 입력합니다')

	args = parser.parse_args()

	return args


#
# get_file_path
#
def get_file_path(file_path):

	if os.path.exists(file_path) != True :
		print("%s 파일이 존재하지 않습니다" % file_path)
		return False
	else:
		return True

#
# load_rgb_image
#
def load_rgb_image(file_path):
	img_frame = cv2.imread(file_path)
	# BGR -> RGB
	rgb_img_frame = cv2.cvtColor(img_frame, cv2.COLOR_BGR2RGB)

	return rgb_img_frame

#
# load_bgr_image
#
def load_bgr_image(file_path):
	img_frame = cv2.imread(file_path)

	return img_frame

#
# play_video
#

def play_video(video_file):

	cap = cv2.VideoCapture(video_file)

	window_name = "Racing Video Windows"	
	#while(cap.isOpened()):
	while True:
		ret, frame = cap.read()
		#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		if ret == True:
			cv2.imshow(window_name,frame)
			cv2.waitKey(30)
		else:
			if cv2.waitKey(0) & 0xFF == ord('q'):
				break

	cap.release()
	cv2.destroyAllWindows()

#
# main program
#
if __name__ == '__main__':

	pp = pprint.PrettyPrinter(indent=4)
	parser = argparse.ArgumentParser()
	args = cmdargs_parsing(parser)
	print(args)

	if get_file_path(args.src):
		play_video(args.src)
