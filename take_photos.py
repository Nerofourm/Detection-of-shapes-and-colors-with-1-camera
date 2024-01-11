import cv2 as cv

cap=cv.VideoCapture(0) #azul , left
cap2=cv.VideoCapture(2) #integrated cam , Right

num=0

while cap.isOpened():
    success1, img =cap.read()
    success2, img2 =cap2.read()

    k=cv.waitKey(5)

    if k == 27:
        break
    elif k == ord('s'):
        cv.imwrite('images/stereoLeft/2L'+str(num)+'.png',img)
        cv.imwrite('images/stereoRight/2R'+str(num)+'.png',img2)
        print('Images saved')
        num +=1

    cv.imshow('left',img)
    cv.imshow('right',img2)

cap.release()
cap2.release()
cv.destroyAllWindows