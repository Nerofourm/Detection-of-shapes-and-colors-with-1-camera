import cv2 as cv
import numpy as np
import pickle

#Aristas internas
aristasx=9
aristasy=6


#Verde Oscuro
gH1=70 #0 a 179
gH2=90


#Azul
bH1=110 #0 a 179
bH2=130

#Rojo
rH1=0 #0 a 179
rH2=20

#Amarillo
yH1=25 #0 a 179
yH2=35

H1=[gH1,bH1,rH1,yH1]
H2=[gH2,bH2,rH2,yH2]

# lower_thres=np.array([H1[0],90,90],#green
#                     [H1[1],90,90], #blue
#                     [H1[2],90,90], #red
#                     [H1[3],90,90]) #yellow

# upper_thres=np.array([H2[0],255,255], #green
#                     [H2[1],255,255], #blue
#                     [H2[2],255,255], #red
#                     [H2[3],255,255]) #yellow

glower_thres=np.array([gH1,90,90])
gupper_thres=np.array([gH2,255,255])

blower_thres=np.array([bH1,90,90])
bupper_thres=np.array([bH2,255,255])



ylower_thres=np.array([yH1,90,90])
yupper_thres=np.array([yH2,255,255])

def getCenter(hsv_image,_H1,_H2,_kernel,_frame):
    _lower_thres=np.array([_H1,90,90])
    _upper_thres=np.array([_H2,255,255])

    _lower_mask=np.array(_lower_thres,dtype="uint8")
    _upper_mask=np.array(_upper_thres,dtype="uint8")

    _mask = cv.inRange(hsv_image,_lower_mask, _upper_mask)

    cv.dilate(_mask,_kernel,_mask,iterations=4)
    cv.erode(_mask,_kernel,_mask,iterations=5)

    _res = cv.bitwise_and(_frame,_frame, mask= _mask)

    _contours, _ =cv.findContours(_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    if len(_contours)>0:
        c=max(_contours,key=cv.contourArea)
        (x, y), radius = cv.minEnclosingCircle(c)
        x=int(x)
        y=int(y)
        #cv.circle(_res,(int(x),int(y)),int(radius),(0,255,0),-1)
        return (x,y)
    else:
        

    # for contour in _contours:
    #         moments= cv.moments(contour)
    #         if moments["m00"] !=0:
    #             cx= int(moments["m10"]/moments["m00"])
    #             cy= int(moments["m01"]/moments["m00"])
    #             cv.drawContours(_res,[contour],-1,(0,255,0),2)
    #             cv.circle(_res,(cx,cy),5,(0,255,0),-1)
    #             cv.putText(_res, "#{}".format(len(_contours) + 1), (cx - 20, cy), cv.FONT_HERSHEY_SIMPLEX,1.0, (255, 255, 255), 2)
        return
    





def main():
    cap=cv.VideoCapture(0) #azul , left
    
    while (cap.isOpened()):
        ret,frame=cap.read()

        hsv_image=cv.cvtColor(frame,cv.COLOR_BGR2HSV)
        kernel=np.ones((3,3),np.uint8)

        greenCenter=getCenter(hsv_image,gH1,gH2,kernel,frame)
        blueCenter=getCenter(hsv_image,bH1,bH2,kernel,frame)
        redCenter=getCenter(hsv_image,rH1,rH2,kernel,frame)
        yellowCenter=getCenter(hsv_image,yH1,yH2,kernel,frame)

        cv.circle(frame,(blueCenter),1,(0,255,0),-1)

        cv.imshow("blue",frame)
        #print(frame)
        #print(type(frame))


        # for contour in contours:
        #     moments= cv.moments(contour)
        #     if moments["m00"] !=0:
        #         cx= int(moments["m10"]/moments["m00"])
        #         cy= int(moments["m01"]/moments["m00"])
        #         cv.circle(res,(cx,cy),5,(0,255,0),-1)
        
        # cv.imshow("Original", frame)
        # cv.imshow("HSV", hsv_image)
        # cv.imshow("Mask", gmask)    
        # cv.imshow("Resultado Final", gres)
        k=cv.waitKey(5)
        if k == 27:
            break



    # with open('images/stereoLeft/Lcamera_params.p','rb') as f:
    #     unpickled=pickle.load(f)
    #     M=unpickled['newCameraMat']
    #     distorsion=unpickled['distorsion']

    # objp= np.zeros((aristasx*aristasy,2),np.float32) #54 rows and 3 columns
    # objp[:,:2] =20*np.mgrid[0:aristasx,0:aristasy].T.reshape(-1,2) #9 rows and 6 col, it will be transposed, 20mm
    # # print(objp[4])        Punto 1 (0,0) Pto 2 (20,0)
    # print(objp)

    #Detección de colores
    cap.release()
    cv.destroyAllWindows
    







    


if __name__=='__main__':
    main()