### Detection of shapes and colors with 1 camera
# By: Nerofourm
# Last Modified: 17-01-2024 

################ IMPORT PACKAGES ################

import cv2 as cv
import numpy as np

################ VARIABLES TO CHANGE ################

cameraPort=2
Z=365  #Distance of the Cam perpendicular to the plane in mm
minimalarea2detect=50
side_detection_accuracy=0.04 #higher, lower precision

################ COLOR VARIABLES ################

font_color=(0,0,0)
red_color=(0,0,255)
green_color=(0,255,0)
blue_color=(255,0,0) 

# lower mask (0-10)
lower_red = np.array([0,50,50])
upper_red = np.array([10,255,255])
# upper mask (170-180)
lower_red1 = np.array([170,50,50])
upper_red1 = np.array([180,255,255])
#
lower_blue = np.array([100,50,50])
upper_blue = np.array([130,255,255])
#
lower_green = np.array([40,50,50])
upper_green = np.array([80,255,255])
#
lower_yellow = np.array([15,40,40]) 
upper_yellow = np.array([40,255,255])

################ CAMERA VARIABLES ################


#Intrinsec Matrix
K=np.array([[1.00625224e+03 ,0.00000000e+00 ,2.98920573e+02],
            [0.00000000e+00, 1.00700371e+03, 2.29296908e+02],
            [0.00000000e+00 ,0.00000000e+00 ,1.00000000e+00]],dtype=np.float64)

fcx=K[0,0] # focal length x
fcy=K[1,1] # focal length y

def main():

    cap=cv.VideoCapture(cameraPort) # 0=Integrated Camera, 2=Blue External Camera

    while (cap.isOpened):
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # Se puede aplicar el filtro gauss tambien puede ir luego de la conversión a gray

        # GAUSSIAN BLUR 
        frame=cv.GaussianBlur(frame,(11,11),0)

        # COLOR TRANSFORMATIONS
        hsv= cv.cvtColor(frame,cv.COLOR_BGR2HSV)
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        masked_img= frame.copy()


        # MASK UNION
        maskred0 = cv.inRange(hsv, lower_red, upper_red)
        maskred1 = cv.inRange(hsv, lower_red1, upper_red1)
        maskblue = cv.inRange(hsv, lower_blue, upper_blue)
        maskgreen = cv.inRange(hsv, lower_green, upper_green)
        maskyellow = cv.inRange(hsv, lower_yellow, upper_yellow)
        maskred = maskred0 + maskred1
        mask=maskyellow+maskgreen+maskblue+maskred
        masked_img[np.where(mask==0)]=0

        cv.imshow('masked',masked_img)

        # RGB IMAGES
        r_img= frame.copy()
        g_img = frame.copy()
        b_img = frame.copy()
        y_img = frame.copy()
    
        r_img[np.where(maskred==0)]=0
        g_img[np.where(maskgreen==0)]=0
        b_img[np.where(maskblue==0)]=0
        y_img[np.where(maskyellow==0)]=0

        # DETECTING THE CONTOURS
        canny=cv.Canny(masked_img,100,200)

        cv.imshow('canny',canny)

        # ERODE AND DILATE THE EDGES
        canny = cv.dilate(canny, None, iterations=1)
        canny = cv.erode(canny, None, iterations=1)
        cv.imshow('ero-canny',canny)
        contours,_ = cv.findContours(canny,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)

        # DETECTION OF COLORS AND SHAPES
        if len(contours)!=0:
            for c in contours:
                # VARIABLE FOR DETECTION
                detected = False
                # REMOVAL OF SMALL OBJECTS BY AREA
                area=cv.contourArea(c)
                if area > minimalarea2detect:
                    # OBTAINING MOMENTS
                    M=cv.moments(c)
                    if M['m00'] != 0:
                        x = int(M['m10']/M['m00'])
                        y = int(M['m01']/M['m00'])

                        # POSITION ESTIMATION
                        X=Z*x/fcx
                        Y=Z*y/fcy
                        X=round(X,2)
                        Y=round(Y,2)
                        
                        # SHAPE DETECTION
                        approx = cv.approxPolyDP(c,side_detection_accuracy*cv.arcLength(c,True),True)
                        
                        # DRAWN NUMBER OF SIDES
                        # cv.putText(canny,str(len(approx)), (x,y+10),1,1.5,(255,255,255),1)
                        # cv.imshow('circle',canny)
                        _,__,w,h=cv.boundingRect(approx)
                        
                        if len(approx)==3:
                            cv.drawContours(frame,[c],0,(0,255,0),2) #Triangulo
                            cv.putText(frame,'Triangulo', (x,y-8),1,1.5,font_color,1)
                            cv.putText(frame,'X:' + str(X), (x,y+10),1,1.5,font_color,1)
                            cv.putText(frame,'Y:' + str(Y), (x,y+28),1,1.5,font_color,1)
                            detected=True
                        elif len(approx)==4:
                            cv.drawContours(frame,[c],0,(0,0,255),2) #Cuadrado
                            aspect_ratio = float(w)/h
                            if aspect_ratio < 1.05 and aspect_ratio > 0.97 :
                                cv.putText(frame,'Cuadrado', (x,y-8),1,1.5,font_color,1)
                            else:
                                cv.putText(frame,'Rectangulo', (x,y-8),1,1.5,font_color,1)
                            cv.putText(frame,'X:' + str(X), (x,y+10),1,1.5,font_color,1)
                            cv.putText(frame,'Y:' + str(Y), (x,y+28),1,1.5,font_color,1)
                            detected=True
                            
                        elif len(approx)==5:
                            cv.drawContours(frame,[c],0,(0,0,255),2) #Pentagono
                            cv.putText(frame,'Pentagono', (x,y-8),1,1.5,font_color,1)
                            cv.putText(frame,'X:' + str(X), (x,y+10),1,1.5,font_color,1)
                            cv.putText(frame,'Y:' + str(Y), (x,y+28),1,1.5,font_color,1)
                            detected=True
                        elif len(approx) > 5 and len(approx) < 9 :
                            cv.drawContours(frame,[c],0,(255,0,0),2) # Circulo
                            cv.putText(frame,'Circulo', (x,y-8),1,1.5,font_color,1)
                            cv.putText(frame,'X:' + str(X), (x,y+10),1,1.5,font_color,1)
                            cv.putText(frame,'Y:' + str(Y), (x,y+28),1,1.5,font_color,1)
                            detected=True
                        
                        
                        # COLOR DETECTION
                        if np.all(r_img[y][x][:] != (0,0,0)) and detected==True:
                            cv.putText(frame,'Rojo', (x,y+46),1,1.5,font_color,1)
                        elif np.all(b_img[y][x][:] != (0,0,0)) and detected==True:
                            cv.putText(frame,'Azul', (x,y+46),1,1.5,font_color,1)
                        elif np.all(g_img[y][x][:] != (0,0,0)) and detected==True:
                            cv.putText(frame,'Verde', (x,y+46),1,1.5,font_color,1)
                        elif np.all(y_img[y][x][:] != (0,0,0)) and detected==True:
                            cv.putText(frame,'Amarillo', (x,y+46),1,1.5,font_color,1)

        #SHOW IMAGES
        cv.imshow('original',frame)

        if cv.waitKey(1) == ord('q'):
            break
    
    cap.release()
    cv.destroyAllWindows()

if __name__=='__main__':
    main()