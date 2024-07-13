import cv2
import pickle

# Kalibrasyon verilerini pickle dosyasından yükleme
with open('calibration_data_50mm_14x16.pkl', 'rb') as f:
    calibration_data = pickle.load(f)

camera_matrix = calibration_data['camera_matrix']
distortion_coefficients = calibration_data['distortion_coefficients']

# Görüntü dosyasının yolunu belirle
image_path = "/home/furkan/Camera Calibration/50mm/test-4.bmp"

# Görüntüyü yükleme
image = cv2.imread(image_path)

if image is not None:
    h, w = image.shape[:2]
    
    # Görüntüyü distorsiyondan arındırma
    undistorted_image = cv2.undistort(image, camera_matrix, distortion_coefficients, None, camera_matrix)

    # Düzeltme sonucunu gösterme
    cv2.imshow('Original Image', cv2.resize(image, (960, 540)))
    cv2.imshow('Undistorted Image', cv2.resize(undistorted_image, (960, 540)))
    cv2.waitKey(5000)  # 5000 milisaniye (5 saniye) bekle
    cv2.destroyAllWindows()

    # Düzeltme sonucunu kaydetme
    cv2.imwrite('undistorted_image10.bmp', undistorted_image)
else:
    print(f"Failed to load the image: {image_path}")
