import camfunctions as cf
import cv2 as cv
import numpy as np

try:
    cam = cv.VideoCapture(0)
except:
    print("camera's not connected")
    cam = cv.VideoCapture(1)


def cameraCheck(cam):
    print("Press q to exit")
    while True:
        ret, frame = cam.read()

        cv.imshow('Camera',frame)

        if cv.waitKey(1) == ord('q'):
            break

def projectorCheck(cam,rows,columns): 
    print("Press q to exit")
    print("Press s to scan for checkerboard")
    map_corners = False
    while True:
        ret, frame = cam.read()

        if map_corners:
            corners1 = np.intp(corners1)
            corners2 = np.intp(corners2)
            frame[corners1[:,1], corners2[:,0]] = [0,0,255]
    
        cv.imshow('Camera',frame)

        if cv.waitKey(1) == ord('q'):
            if map_corners: return corners1,corners2,pixels,lines
            break
        elif cv.waitKey(1) == ord('s'):
            corners1, corners2, pixels, lines = cf.getProjection(rows,columns,frame)
            map_corners = True

def goodzoneCheck(cam,corners1,corners2):
    detector = cv.SimpleBlobDetector()
    print("Press q to exit")
    print("Press d to take a depth map screenshot")
    referencing_depth = False
    detector = cv.SimpleBlobDetector() #Very basic blob dector, will update with trackbars so we can isolate the best settings
    while True:
            ret, frame = cam.read()
            disparity = cf.getDepthMap(frame)
            frame[0:frame.shape[0], 0:int(frame.shape[1]/2)] = cv.polylines(frame[0:frame.shape[0], 0:int(frame.shape[1]/2)], corners1, isClosed=True,color=(0,0,255), thickness=2)
            frame[0:frame.shape[0], int(frame.shape[1]/2):frame.shape[1]] = cv.polylines(frame[0:frame.shape[0], int(frame.shape[1]/2):0], corners1, isClosed=True,color=(0,0,255), thickness=2)
            reg_and_map = np.concatenate((frame,disparity),axis=1)

            if not referencing_depth:
                cv.imshow('Camera',reg_and_map)
            else: 
                keypoints = cf.referenceMaps(detector,reference_disparity.disparity)
                disp_plus_ref = np.concatenate((disparity,reference_disparity),axis=1)
                disp_plus_ref = cv.drawKeypoints(disp_plus_ref,keypoints,0,(255,0,0),flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                cv.imshow('Active vs Reference',disp_plus_ref)
            if cv.waitKey(1) == ord('q'):
                break
            elif cv.waitKey(1) == ord('d'):
                reference_disparity = disparity