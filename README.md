# EMPV 소개

라즈베리파이기반의 donkeycar + deeppicar 교육 프로그램을 위한 코드 repository로 3DEMP의 EMPV1기반에 Donkeycar와 DeepPicar의 운용을 위한 프로그램들이 포함되어 있습니다.
프로그램 동작을 위해서 아래의 환경이 필요합니다.

- Raspberry Pi 3B+ 이상의 보드
- 광각카메라
- 서보모터와 배터리를 탑재한 RC카 샤시
- 무선통신기능 (WiFi)
- 차량조정을 위한 근거리 통신(IR,Bluetooth등)


# 프로그램 폴더 설명

## 01-Google Colab

## 02-OpenCV

## 03-Donkeycar-Training-Colab

## 04-DeepPiCar-NVIDIA-AutoLaneFollow-Colab

## 05-EMPV1-AutoLaneFollow-Colab

## 11-EMPV1-DPCAR

## 99-DONKEYCAR_PARTS


# 프로그램 Copyrights 2020

* Donkeycar는 https://github.com/autorope/donkeycar 를 참고하였습니다.
* DeepPiCar는 https://github.com/dctian/DeepPiCar 를 참고하였습니다. 
* EMPV1에서 Donkeycar와 DeepPiCar를 모두 운영하기 위해서 위의 각각의 소스코드를 수정/변경하였습니다. Donkeycar는 Parts부분중에서 acutator, camera, datastore의 모듈의 소스코드를 수정하였습니다. 아울러, Donkeycar의 제어부분 상에서 DeepPiCar이 동작하도록 하기 위해서 DeepPiCar의 OpenCV Lane Follow 부분과 NVIDIA 모델기반의 Lane Follow 부분의 소스코드를 Donkeycar에서 운영되도록 Donkeycar의 drive파트를 변경하였습니다.  
