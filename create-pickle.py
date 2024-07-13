import cv2
import numpy as np
import glob
import pickle

def calibrate_camera(images, checkerboard_size):
    # 3D noktalar için vektörler
    threedpoints = []
    twodpoints = []

    # 3D gerçek dünya koordinatları
    objectp3d = np.zeros((1, checkerboard_size[0] * checkerboard_size[1], 3), np.float32)
    objectp3d[0, :, :2] = np.mgrid[0:checkerboard_size[0], 0:checkerboard_size[1]].T.reshape(-1, 2)
    prev_img_shape = None

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    
    for filename in images:
        image = cv2.imread(filename)
        
        if image is None:
            print(f"Failed to load the image: {filename}")
            continue
        
        grayColor = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        ret, corners = cv2.findChessboardCorners(
            grayColor, checkerboard_size,
            cv2.CALIB_CB_ADAPTIVE_THRESH +
            cv2.CALIB_CB_FAST_CHECK +
            cv2.CALIB_CB_NORMALIZE_IMAGE)

        if ret:
            threedpoints.append(objectp3d)

            corners2 = cv2.cornerSubPix(
                grayColor, corners, (11, 11), (-1, -1), criteria)

            twodpoints.append(corners2)

            # Köşeleri çizme ve görüntüleme
            image = cv2.drawChessboardCorners(image, checkerboard_size, corners2, ret)
            cv2.imshow('img', cv2.resize(image, (1920, 1080)))
            cv2.waitKey(0)
        else:
            print(f"Cannot find any corners in the image: {filename}")

    cv2.destroyAllWindows()

    if len(threedpoints) > 0 and len(twodpoints) > 0:
        h, w = grayColor.shape[:2]

        ret, matrix, distortion, r_vecs, t_vecs = cv2.calibrateCamera(
            threedpoints, twodpoints, grayColor.shape[::-1], None, None)

        return ret, matrix, distortion, r_vecs, t_vecs
    else:
        print("Not enough points for calibration.")
        return None

images = glob.glob(r"/home/furkan/Camera Calibration/50mm-calibration/*.bmp")

if not images:
    print("No images found.")
else:
    rows = 14
    cols = 16
    checkerboard_size = (rows, cols)
    print(f"Trying checkerboard size: {checkerboard_size}")
    result = calibrate_camera(images, checkerboard_size)
    if result:
        ret, matrix, distortion, r_vecs, t_vecs = result
        if ret:
            print(f"Calibration succeeded for checkerboard size: {checkerboard_size}")
            # Kalibrasyon verilerini pickle dosyasına kaydetme
            calibration_data = {
                'checkerboard_size': checkerboard_size,
                'camera_matrix': matrix,
                'distortion_coefficients': distortion,
                'rotation_vectors': r_vecs,
                'translation_vectors': t_vecs
            }
            with open(f'calibration_data_isometric_{rows}x{cols}.pkl', 'wb') as f:
                pickle.dump(calibration_data, f)
        else:
            print(f"Calibration failed for checkerboard size: {checkerboard_size}")
    else:
        print(f"No valid calibration result for checkerboard size: {checkerboard_size}")

