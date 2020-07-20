#!/usr/bin/env python3
"""
DeepPiCar의 Nvidia Model 학습기반 자율주행
@2020-07-19/Ignitespark

Usage:
    04_dpcar_nvidia_auto_drive.py 

"""
import os
import time
import cv2
from PIL import Image

from docopt import docopt
import numpy as np
import argparse
import json
import pprint

import donkeycar as dk

from tensorflow import keras

# import parts
from donkeycar.parts.transform import Lambda, TriggeredCallback, DelayedTrigger
from donkeycar.parts.datastore import TubHandler
from donkeycar.parts.controller import LocalWebController, JoystickController, WebFpv
from donkeycar.parts.throttle_filter import ThrottleFilter
from donkeycar.parts.behavior import BehaviorPart
from donkeycar.parts.file_watcher import FileWatcher
from donkeycar.parts.launch import AiLaunch
from donkeycar.utils import *
from donkeycar.parts.camera import PiCamera
from donkeycar.parts.image import ImgArrToJpg
from donkeycar.parts.lane_follower import HandCodedLaneFollower
import cv2


#
# model의 구조 출력
#

def print_model(mdl):
    to_json = mdl.to_json()
    pp = pprint.PrettyPrinter()
    pp.pprint(json.loads(to_json))


#
# drive모드 설정하기
#

def drive(cfg, args, camera_type='single',meta=[]):
    model_type = cfg.DEFAULT_MODEL_TYPE
    speed = args.speed
    maxloop = args.maxloop
    model_path = args.model_path

    print("model_path=",model_path)
    print("maxloop=",maxloop,",speed=",speed)

###########################################################
# 1) 동키카를 초기화(donkey사용을 위한 환경 설정)
###########################################################
    V = dk.vehicle.Vehicle()

###########################################################
# 2) 주행환경 설정하기
###########################################################
    class EnvSetting(object):
        def __init__(self, mode='user', throttle=12): # 12%
            self.mode = mode
            self.throttle = throttle * 0.01

        def run(self):
            return self.mode, self.throttle

    V.add(EnvSetting(throttle=speed),inputs=[], outputs=['user/mode','user/throttle'])

###########################################################
# 3) 카메라 설정(PICAM)
###########################################################
    print("cfg.CAMERA_TYPE", cfg.CAMERA_TYPE)

    inputs = []
    threaded = True
    car_mode = 'nvidia'

    dpcar_opt = { 'org' : True, 'hsv' : False, 'edges' : False, 'lanes': False }
    if cfg.CAMERA_TYPE == "PICAM":
        cam = PiCamera(image_w=cfg.IMAGE_W, image_h=cfg.IMAGE_H, image_d=cfg.IMAGE_DEPTH, framerate=cfg.CAMERA_FRAMERATE, \
        vflip=cfg.CAMERA_VFLIP, hflip=cfg.CAMERA_HFLIP,mode=car_mode, dpcar_opt=dpcar_opt)
        print(cfg.IMAGE_H, "x", cfg.IMAGE_W)

    else:
        raise(Exception("Unkown camera type: %s" % cfg.CAMERA_TYPE))

    if car_mode == 'deepicar':
        V.add(cam, inputs=inputs, outputs=['cam/image_array','user/angle'], threaded=threaded)
    else:
        V.add(cam, inputs=inputs, outputs=['cam/image_array'], threaded=threaded)

###########################################################
# 4) 주행기록저장을 위한 클래스 생성 및 V.add()
###########################################################
    class RecordTracker:
        def __init__(self):
            self.last_num_rec_print = 0
            self.dur_alert = 0
            self.force_alert = 0

        def run(self, num_records):
            print("num_records=>",num_records)

            if num_records is None:
                return 0

            if self.last_num_rec_print != num_records or self.force_alert:
                self.last_num_rec_print = num_records

                if num_records % 10 == 0:
                    print("recorded", num_records, "records")

                if num_records % cfg.REC_COUNT_ALERT == 0 or self.force_alert:
                    self.dur_alert = num_records // cfg.REC_COUNT_ALERT * cfg.REC_COUNT_ALERT_CYC
                    self.force_alert = 0

            if self.dur_alert > 0:
                self.dur_alert -= 1

            if self.dur_alert != 0:
                return get_record_alert_color(num_records)

            return 0

    rec_tracker_part = RecordTracker()
    V.add(rec_tracker_part, inputs=["tub/num_records"], outputs=['records/alert'])


####################################################################
#
# Nvidia 자율주행을 위한 모델을 로딩하고, 이미지 변환
# (320x240) -> (200,66) 컬러이미지로 변환
#
####################################################################

    class NVidiaKerasLinear():
        def __init__(self,model_path=None,throttle=12,verbose=False):
            self.mdl = keras.models.load_model(model_path)
            self.throttle = throttle * 0.01
            if verbose:
                print(self.mdl.summary())

        def control_to_degree(self,ctl):
            degree = ctl * 40 + 90
            return degree

        def degree_to_control(self,drg):
            ctl = (drg - 90) * (1/40)
            return ctl
       
        def predict_by_model(self,image):
            y_pred = self.mdl.predict(image)
            return y_pred

        def img_preprocess(self,image):
            height, _, _ = image.shape
            image = image[int(height/2):,:,:]
            image = cv2.cvtColor(image, cv2.COLOR_RGB2YUV)
            image = cv2.GaussianBlur(image, (3,3), 0)
            image = cv2.resize(image, (200,66))
            image = image / 255 

            return image


        def run(self,img_arr):
            if img_arr is None:
                    print("no image")
                    return 'user', 0.0, self.throttle # 90 degree
         
            print("image_arr.shape=",np.array(img_arr).shape)

            # nvidia 모델에서 사용하는image format으로 변환 (60,300,3)
            nvidia_image = self.img_preprocess(img_arr)

            print("nvidia_image = ",nvidia_image.shape)
            nvidia_image_expd = np.expand_dims(nvidia_image,axis=0)
            print("nvidia_image_expand=",nvidia_image_expd.shape)

            degree_pred = self.predict_by_model(nvidia_image_expd)
            ctrl_pred = self.degree_to_control(degree_pred)

            return 'user', ctrl_pred ,self.throttle


        def shutdown(self):
            pass


    # 자율주행을 위한 모델로딩
    kl = NVidiaKerasLinear(model_path,throttle=speed,verbose=True)
    V.add(kl,inputs=['cam/image_array'], outputs=['user/mode','user/angle','user/throttle']) 

###########################################################
# 5) DriveMode 설정하기
###########################################################
#Choose what inputs should change the car.
    class DriveMode:
        def run(self, mode, user_angle, user_throttle, pilot_angle, pilot_throttle):
            if mode == 'user':
                print("user_angle->",user_angle,", user_throttle->",user_throttle)
                return user_angle, user_throttle, True

            elif mode == 'local_angle':
                return pilot_angle if pilot_angle else 0.0, user_throttle, True

            else:
                return pilot_angle if pilot_angle else 0.0, pilot_throttle * cfg.AI_THROTTLE_MULT if pilot_throttle else 0.0, True

    V.add(DriveMode(), inputs=['user/mode', 'user/angle', 'user/throttle', 'pilot/angle', 'pilot/throttle'], outputs=['angle', 'throttle','recording'])

###########################################################
# 6) PIGPIO_PWM 설정하기
# - 현재 EMPV1에서는 "DC_STREER_THROTTLE를 사용
###########################################################

    if cfg.DRIVE_TRAIN_TYPE == "DC_STEER_THROTTLE":
        from donkeycar.parts.actuator import Mini_HBridge_DC_Motor_PWM
        from donkeycar.parts.actuator import RPi_GPIO_Servo
 
        #steering = Mini_HBridge_DC_Motor_PWM(cfg.HBRIDGE_PIN_LEFT, cfg.HBRIDGE_PIN_RIGHT)
        steering = RPi_GPIO_Servo(cfg.HBRIDGE_PIN_RIGHT,verbose=False)
        throttle = Mini_HBridge_DC_Motor_PWM(cfg.HBRIDGE_PIN_FWD, cfg.HBRIDGE_PIN_BWD)

        print(">>>>DC_STEER_THROTTLE")
        V.add(steering, inputs=['angle'])
        V.add(throttle, inputs=['throttle'])

###########################################################
# 7) Tub 설정하기
###########################################################

    inputs=['cam/image_array', 'user/angle', 'user/throttle', 'user/mode']
    types=['image_array', 'float', 'float', 'str']

    th = TubHandler(path=cfg.DATA_PATH)
    tub = th.new_tub_writer(inputs=inputs, types=types, user_meta=meta)
    V.add(tub, inputs=inputs, outputs=["tub/num_records"], run_condition='recording')


###########################################################3yy
# 8) V.start (Main Loop)
###########################################################

    #V.start(rate_hz=cfg.DRIVE_LOOP_HZ, max_loop_count=cfg.MAX_LOOPS)
    V.start(rate_hz=cfg.DRIVE_LOOP_HZ, max_loop_count=maxloop)


#
#
# main program
#

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path',help='.h5 nvidia model path')
    parser.add_argument('--myconfig', default='myconfig.py', help='configuration file')
    parser.add_argument('--speed', type=int, default=12, help='speed percentage')
    parser.add_argument('--maxloop', type=int, default=200, help='max loop coount')

    args = parser.parse_args()
    print(args)

    cfg = dk.load_config(myconfig=args.myconfig)
    drive(cfg,args)
