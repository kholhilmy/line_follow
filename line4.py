import cv2
import numpy as np
import time
# value warna
#hsvval = [0, 0, 117,179, 22, 219]
#lower = np.array([hsvval[0],hsvval[1],hsvval[2]])
#upper = np.array([hsvval[3],hsvval[4],hsvval[5]])
sensors = 3

# inisialisasi kamera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

while True:
    ret, frame = cap.read()
    
    
    frames= np.vsplit(frame,sensors)
    for yoi, im in enumerate(frames):
        #print(frames[0])
        #time.sleep(10)
        #print("SELESAI")
        #time.sleep(10)
        gray= cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        ret,binary = cv2.threshold(gray,1,255,cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)
        
        #height,width, = binary.shape
        #mask = np.zeros_like(binary)
        mask_or=cv2.bitwise_and(im,im,mask=binary)
        
        # menganalisis bentuk dan deteksi objek
        contours, hierachry = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        for cnt in contours:
            
            biggest=max(contours,key=cv2.contourArea)
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.drawContours(im, contours,-1,(255,0,255),3)
            
            cx = x+w //2
            cy = y+h //2
            cv2.circle(im,(cx,cy),8,(0,255,0),cv2.FILLED)    
            cv2.imshow(str(yoi),im)
            
            for cx0 in frame[0]:
                cx0 =cx- 320
                for cx2 in frame[2]:
                    cx2 =cx- 320
                    if cx0 <0 & cx2>0:
                        print("KANAN")
                    elif cx0>0 & cx2<0:
                        print("KIRI")
                    
            '''        
            if frames[0] == frames[0]:
                cx0 =cx- 320
                if frames[2]:
                    cx2 =cx- 320
                    if cx0>0 & cx2<0:
                        print("KIRI")
                    elif cx0<0 & cx2>0:
                        print("KANAN")'''
                            
            

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
