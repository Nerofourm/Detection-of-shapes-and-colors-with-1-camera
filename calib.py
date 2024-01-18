import cv2 as cv
import numpy as np
import glob
import pickle
import matplotlib.pyplot as plt

#Aristas internas
aristasx=9
aristasy=6

#Criterio para detectar las esquinas internas
criteria=(cv.TERM_CRITERIA_EPS+cv.TERM_CRITERIA_MAX_ITER,100,0.001)

#Define the object points, each square has 20 mm
objp= np.zeros((aristasx*aristasy,3),np.float32) #54 rows and 3 columns
objp[:,:2] =20*np.mgrid[0:aristasx,0:aristasy].T.reshape(-1,2) #9 rows and 6 col, it will be transposed, 20mm
#print(objp)

#Array to store object and image points 
objpoints=[]
imgpoints=[]

images=glob.glob('images/stereoLeft/*.png') #  Left Blue Camera Images
print(len(images))
for fname in images:
    img =cv.imread(fname)
    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    #Find corners
    find, corners = cv.findChessboardCorners(gray,(aristasx,aristasy),None)
    if not find:
        print('Image ',fname,' not uploaded')
        break

    if find==True:
        objpoints.append(objp)

        corners2=cv.cornerSubPix(gray,corners,(5,5),(-1,-1),criteria)
        imgpoints.append(corners2)

        #Draw
        img=cv.drawChessboardCorners(img,(aristasx,aristasy),corners2,find)
        cv.imshow('img',img)
        cv.waitKey(100)

    else:
        print("find False")

ret,cameraMat,distorsion,rvecs,tvecs = cv.calibrateCamera(objpoints,imgpoints,gray.shape[::-1],None,None)
print('ret')
print(ret)
print('cameraMat')
print(cameraMat)
print('distorsion')
print(distorsion)
print('rvecs')
print(rvecs)
print('tvecs')
print(tvecs)

#Save the values 
dist_pickle={}
dist_pickle['ret']=ret
dist_pickle['cameraMat']=cameraMat
dist_pickle['distorsion']=distorsion
dist_pickle['rvecs']=rvecs
dist_pickle['tvecs']=tvecs

pickle.dump(dist_pickle, open('images/stereoLeft/Lcamera_params.p','wb'))


# undistortion (Through cv.undistort)
img = cv.imread('images/stereoLeft/L5.png')
h,  w = img.shape[:2]
newcameramtx, roi = cv.getOptimalNewCameraMatrix(cameraMat, distorsion, (w,h), 1, (w,h))
img_undist = cv.undistort(img, cameraMat, distorsion,None,newcameramtx)
print("ROI")
print(roi)
print('newCameraMat')
print(newcameramtx)

dist_pickle['newCameraMat']=newcameramtx
pickle.dump(dist_pickle, open('images/stereoLeft/Lcamera_params.p','wb'))

#Crop the image

x, y, w, h = roi
img_undist = img_undist[y:y+h, x:x+w]
cv.imwrite('images/stereoLeft/Lcalibresult.png', img_undist)

mean_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], cameraMat, distorsion)
    error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
    mean_error += error
print( "total error: {}".format(mean_error/len(objpoints)) )

# Visualize undistortion
cv.imshow('Con distorsion',img)
cv.imshow('Sin distorsion',img_undist)
cv.waitKey(0)



cv.destroyAllWindows()