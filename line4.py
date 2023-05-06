import cv2
import numpy as np

# value warna
hsvval = [0, 0, 117,179, 22, 219]
lower = np.array([hsvval[0],hsvval[1],hsvval[2]])
upper = np.array([hsvval[3],hsvval[4],hsvval[5]])
sensors = 3

# inisialisasi kamera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

while True:
    ret, frame = cap.read()
    gray= cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    ret,binary = cv2.threshold(gray,1,255,cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)
    
    height,width, = binary.shape
    mask = np.zeros_like(binary)
    mask_or=cv2.bitwise_and(frame,frame,binary)

    # menganalisis bentuk dan deteksi objek
    contours, hierachry = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    centxer = 0
    biggest=max(contours,key=cv2.contourArea)
    cv2.drawContours(frame, contours,-1,(255,0,255),7)
    x,y,w,h = cv2.boundingRect(biggest)
    cx = x+w //2
    cy = y+h //2
    cv2.circle(frame,(cx,cy),10,(0,255,0),cv2.FILLED)

    
    frames= np.vsplit(mask_or,sensors)
    for y, im in enumerate(frames):
        cv2.imshow(str(im),y)

    # menampilkan hasil pada layar
    cv2.imshow("layar",frame)
    cv2.imshow("Deteksi Warna", mask_or)


    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
