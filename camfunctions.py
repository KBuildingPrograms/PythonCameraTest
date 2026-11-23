#Cameratesting Functions

import cv2 as cv
import glob
import numpy as np

#calibration based on tutorial by Dr. Temuge Batpurev, https://temugeb.github.io/opencv/python/2021/02/02/stereo-camera-calibration-and-triangulation.html
def generalCalibrate(images_path,camera): #calibrating the camera's sense of scale
    #0 for left, 1 for right (aka false for left, true for right)
    image_names = sorted(glob.glob(images_path))
    images = []
    for imname in image_names:
        im = cv.imread(imname,1) 
        im = im[0:im.shape[0],int(im.shape[1]/2):im.shape[1]] if camera else im[0:im.shape[0],0:int(im.shape[1]/2)]
        images.append(im)
    try:
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    except:
        return 0
    rows = 6
    columns = 9
    scaling = 1. #change to the size of square in mm

    objp = np.zeros((rows*columns,3), np.float32) #for coordinates
    objp[:,:2] = np.mgrid[0:rows,0:columns].T.reshape(-1,2)
    objp = scaling*objp 

    imgpoints = []
    objpoints = []

    for frame in images:
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
 
        #find the checkerboard
        ret, corners = cv.findChessboardCorners(gray, (rows, columns), None)
 
        if ret == True:
 
            #Convolution size used to improve corner detection. Don't make this too large.
            conv_size = (11, 11)
 
            #opencv can attempt to improve the checkerboard coordinates
            corners = cv.cornerSubPix(gray, corners, conv_size, (-1, -1), criteria)
            cv.drawChessboardCorners(frame, (rows,columns), corners, ret)
            cv.imshow('img', frame)
            k = cv.waitKey(500)
 
            objpoints.append(objp)
            imgpoints.append(corners)
    image_ref = images[0]

    width = image_ref.shape[1]
    height = image_ref.shape[0]

    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, (width,height), None, None)
    return mtx, dist #cameramatrix and distortion coefficients


def stereoCalibrate(mtx1,dist1,mtx2,dist2,frames):
    c1_images = []
    c2_images = []
    for frame in frames:
        c2 = frame[0:frame.shape[0],int(frame.shape[1]/2):frame.shape[1]]
        c2_images.append(c2)
        c1 = frame[0:frame.shape[0],0:int(frame.shape[1]/2)]
        c1_images.append(c1)
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.0001)

    rows = 6
    columns = 9
    scaling = 1. #change to the size of square in mm

    objp = np.zeros((rows*columns,3), np.float32)
    objp[:,:2] = np.mgrid[0:rows,0:columns].T.reshape(-1,2)
    objp = scaling*objp

    #frame dimensions. Frames should be the same size.
    width = c1_images[0].shape[1]
    height = c1_images[0].shape[0]
 
    #Pixel coordinates of checkerboards
    imgpoints_left = [] # 2d points in image plane.
    imgpoints_right = []
 
    #coordinates of the checkerboard in checkerboard world space.
    objpoints = [] # 3d point in real world space
 
    for frame1, frame2 in zip(c1_images, c2_images):
        gray1 = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
        gray2 = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)
        c_ret1, corners1 = cv.findChessboardCorners(gray1, (5, 8), None)
        c_ret2, corners2 = cv.findChessboardCorners(gray2, (5, 8), None)
 
        if c_ret1 == True and c_ret2 == True:
            corners1 = cv.cornerSubPix(gray1, corners1, (11, 11), (-1, -1), criteria)
            corners2 = cv.cornerSubPix(gray2, corners2, (11, 11), (-1, -1), criteria)
 
            cv.drawChessboardCorners(frame1, (5,8), corners1, c_ret1)
            cv.imshow('img', frame1)
 
            cv.drawChessboardCorners(frame2, (5,8), corners2, c_ret2)
            cv.imshow('img2', frame2)
            k = cv.waitKey(500)
 
            objpoints.append(objp)
            imgpoints_left.append(corners1)
            imgpoints_right.append(corners2)
 
    stereocalibration_flags = cv.CALIB_FIX_INTRINSIC
    ret, CM1, dist1, CM2, dist2, R, T, E, F = cv.stereoCalibrate(objpoints, imgpoints_left, imgpoints_right, mtx1, dist1,
                                                                 mtx2, dist2, (width, height), criteria = criteria, flags = stereocalibration_flags)

    return R,T # 3x1 rotation vector, 3x1 translation vector

from blending_utils.libs.dlpc754x import commands as cmds
def getProjection(rows,columns,frame): #returns the corners based on each camera's perspective and the dimensions of the projector
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    gray1 = cv.cvtColor(frame[0:frame.shape[0],0:int(frame.shape[1]/2)], cv.COLOR_BGR2GRAY)
    gray2 = cv.cvtColor(frame[0:frame.shape[0],int(frame.shape[1]/2):frame.shape[1]], cv.COLOR_BGR2GRAY)
    Summary, DisplayImageSize = cmds.ReadDisplayImageSize()
    if Summary.Successful: #pixels are columns, lines are rows
        pixels = DisplayImageSize.DisplayAreaPixelsPerLine 
        lines = DisplayImageSize.DisplayAreaLinesPerFrame
    else:
        pixels = 3840
        lines = 2160 #default resolution from vincent's code
    
    pattern = (rows-1, columns-1)
    ret1, corners1 = cv.findChessboardCorners(gray1,pattern,None)
    ret2, corners2 = cv.findChessboardCorners(gray2,pattern,None)
    if ret1:
        refined_corners1 = cv.cornerSubPix(gray1,corners1,(11,11),(-1,-1),criteria)
    if ret2: 
        refined_corners2 = cv.cornerSubPix(gray2,corners2,(11,11),(-1,-1),criteria)

    if refined_corners1 != None and refined_corners2 != None:
        return refined_corners1, refined_corners2, pixels, lines
    return 0, 0, pixels, lines

def getDepthMap(frame):
    gray1 = cv.cvtColor(frame[0:frame.shape[0],0:frame.shape[1]],cv.COLOR_BGR2GRAY)
    gray2 = cv.cvtColor(frame[0:frame.shape[0],int(frame.shape[1]/2):frame.shape[1]], cv.COLOR_BGR2GRAY)

    stereo = cv.StereoBM.create(numDisparities=16,blockSize=15) #can alter for clarity
    disparity = stereo.compute(gray1,gray2)

    return disparity

def referenceMaps(detector, reference_map, current_map):
    difference = cv.absdiff(reference_map,current_map)
    mask = cv.cvtColor(difference,cv.COLOR_BGR2GRAY)
    keypoints = detector.detect(mask)
    return keypoints


    