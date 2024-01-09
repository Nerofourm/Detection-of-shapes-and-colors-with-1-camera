import cv2 as cv
import numpy as np 

def main():
    cap=cv.VideoCapture(0)
    while(True):
        ret,img=cap.read()
        max=500
        corner_count=150

        #path= '/home/espectro/Downloads/imagenes_/imagen6.bmp'

        #img=cv.imread(path)
        #print(img.shape)
        #cv.imshow("tablero",img)
        mono=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
        #cv.imshow("Mono",mono)

        corners=cv.goodFeaturesToTrack(mono,max,0.25,15)
        corners_int=corners.astype(int)
        #print('Esquinas detectadas: ', len(corners))
        img2=img

        for i in range(len(corners_int)):
            cv.circle(img2,(corners_int[i][0][0],corners_int[i][0][1]),3,(0,0,255))

        cv.imshow("GFT",img2)


        key = cv.waitKey(1)
        if key == 27:  # Press 'Esc' to exit
            break


    cap.release()
    cv.destroyAllWindows()

if __name__=='__main__':
    main()
