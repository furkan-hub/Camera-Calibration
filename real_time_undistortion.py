import cv2 
import numpy as np
import pickle
import time
from hik_camera.hik_camera import HikCamera

import cv2

ips = HikCamera.get_all_ips()

print("All camera IP adresses:", ips)
ip = ips[0]

cam = HikCamera(ip=ip)

# cam = HikCamera(ip=ip)

# cap = cv2.VideoCapture(1)
# # Çözünürlüğü ayarla
# # height: 3648
# # width: 5472
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 4656)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 3496)

# FPS'i ayarla
#cap.set(cv2.CAP_PROP_FPS, 1)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Chessboard dimensions
pattern_size = (8,6)
objp = np.zeros((pattern_size[0] * pattern_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2)

objpoints = []  # 3D points in real world space
imgpoints = []  # 2D points in image plane

min_samples_for_calibration = 15  # Minimum number of samples needed for calibration
with cam:
    cam["ExposureAuto"] = "Off"
    cam["ExposureTime"] = 168724.0000
    while True:
        frame = cam.robust_get_frame()


        frame_copy = np.copy(frame)  # Create a copy of the frame
        time.sleep(1)

        #gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        found, corners = cv2.findChessboardCorners(frame, pattern_size)
        if found:
            corners2 = cv2.cornerSubPix(frame, corners, (11, 11), (-1, -1), criteria)
            objpoints.append(objp)
            imgpoints.append(corners2)
            cv2.drawChessboardCorners(frame, pattern_size, corners2, found)
            print(f"Found {len(objpoints)} samples")
        else:
            print("cant find any corner")
            break

        cv2.imshow("Webcam (Processed)", cv2.resize(frame, (1900, 1200)))
        cv2.imshow("Webcam (Original)", frame_copy)  # Show the unprocessed image

        if cv2.waitKey(30) & 0xFF == ord("q"):
            break

        # Calibrate after collecting enough samples
        # if len(objpoints) >= min_samples_for_calibration:
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, frame.shape[::-1], None, None)

        if ret:
            # Save calibration results
            with open('calibration_data.pkl', 'wb') as f:
                pickle.dump((mtx, dist), f)             

            # Print camera calibration results
            print("Camera matrix:", mtx)
            print("Distortion coefficients:", dist)

            # Calculate and print the re-projection error
            total_error = 0
            for i in range(len(objpoints)):
                imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
                error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
                total_error += error

            print("Total re-projection error:", total_error / len(objpoints))

            # Demonstrate the undistortion on the last captured frame
            undistorted_img = cv2.undistort(frame_copy, mtx, dist, None, mtx)
            blur = cv2.blur(undistorted_img, (3, 3))
            cv2.imshow("Undistorted Image", cv2.resize(blur, (1900, 1200)))
        
        else:
            print("Calibration was unsuccessful. Please try again.")
        break

cv2.destroyAllWindows()
