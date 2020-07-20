#!/usr/bin/env python3
"""
Donkeycar의 하위제어모듈을 연동한 기본 프로그램 
- donkeycar의 manage.py에서 필수적인 모듈만으로 구성한 운행프로그램
- DeepPiCar의 제어를 위해서 사용
@2020-07-13/Ignitespark

Usage:
    01_dpcar_drive.py [--myconfig=<filename>]


Options:
    -h --help               Show this screen.
    -f --file=<file>        A text file containing paths to tub files, one per line. Option may be used more than once.
    --myconfig=filename     Specify myconfig file to use.
                            [default: myconfig.py]
"""
import os
import time
import cv2
from PIL import Image

from docopt import docopt
import numpy as np

import donkeycar as dk

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

#
# drive모드 설정하기
#

def drive(cfg, model_type=None, camera_type='single',meta=[]):
    model_type = cfg.DEFAULT_MODEL_TYPE

###########################################################
# 1) 동키카를 초기화(donkey사용을 위한 환경 설정)
###########################################################
    V = dk.vehicle.Vehicle()

###########################################################
# 2) 카메라 설정(PICAM)
###########################################################
    print("cfg.CAMERA_TYPE", cfg.CAMERA_TYPE)

    inputs = []
    threaded = True
    if cfg.CAMERA_TYPE == "PICAM":
        cam = PiCamera(image_w=cfg.IMAGE_W, image_h=cfg.IMAGE_H, image_d=cfg.IMAGE_DEPTH, framerate=cfg.CAMERA_FRAMERATE, \
        vflip=cfg.CAMERA_VFLIP, hflip=cfg.CAMERA_HFLIP,mode='deepicar')
        print(cfg.IMAGE_H, "x", cfg.IMAGE_W)

    else:
        raise(Exception("Unkown camera type: %s" % cfg.CAMERA_TYPE))

    V.add(cam, inputs=inputs, outputs=['cam/image_array','user/dpc_angle'], threaded=threaded)


###########################################################
# 3) 웹컨트롤러 설정하기
###########################################################

    ctr = LocalWebController(port=cfg.WEB_CONTROL_PORT, mode=cfg.WEB_INIT_MODE)
    
    V.add(ctr, inputs=['cam/image_array', 'tub/num_records'], outputs=['user/angle', 'user/throttle', 'user/mode', 'recording'], threaded=True)

###########################################################
# 4) 주행기록저장을 위한 클래스 생성 및 V.add()
###########################################################
    class RecordTracker:
        def __init__(self):
            self.last_num_rec_print = 0
            self.dur_alert = 0
            self.force_alert = 0

        def run(self, num_records):
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


###########################################################
# 5) DriveMode 설정하기
###########################################################
#Choose what inputs should change the car.
    class DriveMode:
        def run(self, mode, user_angle, user_throttle, pilot_angle, pilot_throttle):
            if mode == 'user':
                #print("user_angle->",user_angle,", user_throttle->",user_throttle)
                return user_angle, user_throttle

            elif mode == 'local_angle':
                return pilot_angle if pilot_angle else 0.0, user_throttle

            else:
                return pilot_angle if pilot_angle else 0.0, pilot_throttle * cfg.AI_THROTTLE_MULT if pilot_throttle else 0.0 

    V.add(DriveMode(), inputs=['user/mode', 'user/angle', 'user/throttle', 'pilot/angle', 'pilot/throttle'], outputs=['angle', 'throttle'])

###########################################################
# 6) PIGPIO_PWM 설정하기
# - 현재 EMPV1에서는 "DC_STREER_THROTTLE를 사용
###########################################################
    '''
    if cfg.DRIVE_TRAIN_TYPE == "PIGPIO_PWM":
        from donkeycar.parts.actuator import PWMSteering, PWMThrottle, PiGPIO_PWM
        steering_controller = PiGPIO_PWM(cfg.STEERING_PWM_PIN, freq=cfg.STEERING_PWM_FREQ, inverted=cfg.STEERING_PWM_INVERTED)
        steering = PWMSteering(controller=steering_controller, left_pulse=cfg.STEERING_LEFT_PWM, right_pulse=cfg.STEERING_RIGHT_PWM)

        throttle_controller = PiGPIO_PWM(cfg.THROTTLE_PWM_PIN, freq=cfg.THROTTLE_PWM_FREQ, inverted=cfg.THROTTLE_PWM_INVERTED)
        throttle = PWMThrottle(controller=throttle_controller, max_pulse=cfg.THROTTLE_FORWARD_PWM,  \
                    zero_pulse=cfg.THROTTLE_STOPPED_PWM, min_pulse=cfg.THROTTLE_REVERSE_PWM)

        print(">>>>>PIGPIO_PWM")
        V.add(steering, inputs=['angle'], threaded=True)
        V.add(throttle, inputs=['throttle'], threaded=True)
    '''

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


###########################################################
# 8) WebServerController 설정하기
# - 공개하지 않으면(PUB_CAMERA_IMAGES), 아래의 코드는 동작하기 않음
# - 다만, 어떻게 웹서비스에 접속할지에 대한 내용은 유효
###########################################################

    if type(ctr) is LocalWebController:
        if cfg.DONKEY_GYM:
            print("You can now go to http://localhost:%d to drive your car." % cfg.WEB_CONTROL_PORT)
        else:
            print("You can now go to <your hostname.local>:%d to drive your car." % cfg.WEB_CONTROL_PORT)


###########################################################3yy
# 9) V.start (Main Loop)
###########################################################

    V.start(rate_hz=cfg.DRIVE_LOOP_HZ, max_loop_count=cfg.MAX_LOOPS)


#
#
# main program
#

if __name__ == '__main__':
    args = docopt(__doc__)
    cfg = dk.load_config(myconfig=args['--myconfig'])

    drive(cfg)
