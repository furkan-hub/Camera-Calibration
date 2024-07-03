import cv2
import pickle
from hik_camera.hik_camera import HikCamera

ips = HikCamera.get_all_ips()
print("All camera IP addresses:", ips)

if len(ips) == 0:
    print("No cameras found")
    exit(1)

ip = ips[0]
cam = HikCamera(ip=ip)

# Load calibration data
with open(r'/home/furkan/Camera Calibration/calibration_data.pkl', 'rb') as f:
    mtx, dist = pickle.load(f)

with cam:
    cam["ExposureAuto"] = "Off"
    cam["ExposureTime"] = 129159

    while True:
        frame = cam.robust_get_frame()  # Get only the frame
        if frame is None:
            print("Failed to capture frame")
            break

        # Undistort the frame
        undistorted_frame = cv2.undistort(frame, mtx, dist, None, mtx)
        blur = cv2.blur(undistorted_frame, (5, 5))

        # Show original and undistorted frames
        cv2.imshow('Original', cv2.resize(frame, (900, 600)))
        cv2.imshow('Undistorted', cv2.resize(blur, (900, 600)))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cv2.destroyAllWindows()
