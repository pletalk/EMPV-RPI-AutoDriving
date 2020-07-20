import cv2

seqno = 0
filename ='/home/pi/tmp_data/kk-%03d.jpg' % (seqno)

print(filename)
img = cv2.imread(filename)


cv2.imshow('test',img)
cv2.waitKey(0)
