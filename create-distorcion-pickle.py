import cv2
import numpy as np
import glob
import pickle

CHECKERBOARD = (18, 27)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# 3D noktalar için vektörler
threedpoints = []
twodpoints = []

# 3D gerçek dünya koordinatları
objectp3d = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objectp3d[0, :, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
prev_img_shape = None

# Görüntü dosyalarını bulmak için glob kullanma
images = glob.glob(r"/home/furkan/Camera Calibration/images/dist-cal.bmp")

if not images:
    print("No images found.")
else:
    for filename in images:
        image = cv2.imread(filename)
        
        if image is None:
            print(f"Failed to load the image: {filename}")
            continue
        
        grayColor = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        ret, corners = cv2.findChessboardCorners(
            grayColor, CHECKERBOARD,
            cv2.CALIB_CB_ADAPTIVE_THRESH +
            cv2.CALIB_CB_FAST_CHECK +
            cv2.CALIB_CB_NORMALIZE_IMAGE)

        if ret:
            threedpoints.append(objectp3d)

            corners2 = cv2.cornerSubPix(
                grayColor, corners, (11, 11), (-1, -1), criteria)

            twodpoints.append(corners2)

            # Köşeleri çizme ve görüntüleme
            image = cv2.drawChessboardCorners(image, CHECKERBOARD, corners2, ret)
            cv2.imshow('img', cv2.resize(image, (1920, 1080)))
            cv2.waitKey(0)
        else:
            print(f"Cannot find any corners in the image: {filename}")

    cv2.destroyAllWindows()

    if len(threedpoints) > 0 and len(twodpoints) > 0:
        h, w = grayColor.shape[:2]

        ret, matrix, distortion, r_vecs, t_vecs = cv2.calibrateCamera(
            threedpoints, twodpoints, grayColor.shape[::-1], None, None)

        # Kalibrasyon verilerini pickle dosyasına kaydetme
        calibration_data = {
            'camera_matrix': matrix,
            'distortion_coefficients': distortion,
            'rotation_vectors': r_vecs,
            'translation_vectors': t_vecs
        }

        with open('calibration_data.pkl', 'wb') as f:
            pickle.dump(calibration_data, f)

        # Gerekli çıktıyı gösterme
        print("Camera matrix:")
        print(matrix)

        print("\nDistortion coefficient:")
        print(distortion)

        print("\nRotation Vectors:")
        print(r_vecs)

        print("\nTranslation Vectors:")
        print(t_vecs)
    else:
        print("Not enough points for calibration.")
