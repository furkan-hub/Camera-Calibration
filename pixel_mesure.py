import cv2
import numpy as np
import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt

# Tıklanan noktaları saklamak için liste
points = []

# Mesafeleri saklamak için liste
distances = []

# Fare tıklama olayını işleyen işlev
def click_event(event, x, y, flags, params):
    global points, distances
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        cv2.circle(img, (x, y), 0, (0, 255, 0), -1)
        cv2.imshow('image', img)
        if len(points) == 2:
            distance = np.linalg.norm(np.array(points[0]) - np.array(points[1])) * 0.085
            pixel = np.linalg.norm(np.array(points[0]) - np.array(points[1]))
            print(f'Tıklanan iki nokta arasındaki mesafe: {distance} mm')
            print(f'Tıklanan iki nokta arasındaki piksel: {pixel} px')
            distances.append(distance)
            points = []

# Bir görüntü yükleyin
img = cv2.imread('50mm/test-5.bmp')

# Pencere boyutunu belirleyin
window_name = 'image'
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window_name, 800, 600)  # Pencere boyutunu ayarlayın

# Görüntüyü ekranda gösterin
cv2.imshow(window_name, img)

# Fare tıklama olayını pencereye bağlayın
cv2.setMouseCallback(window_name, click_event)

# ESC tuşuna basılana kadar bekleyin
cv2.waitKey(0)
cv2.destroyAllWindows()

# Geçerli tarih ve saati al
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

# Klasör adı oluştur
folder_name = f'test_{current_time}'
os.makedirs(folder_name, exist_ok=True)

# CSV dosya adı ve yolu oluştur
csv_filename = 'distances.csv'
csv_filepath = os.path.join(folder_name, csv_filename)

# Mesafeleri CSV dosyasına kaydetme
with open(csv_filepath, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Distance (mm)"])
    for distance in distances:
        writer.writerow([distance])

# Mesafeleri grafik olarak görselleştirme
plt.figure(figsize=(10, 6))
plt.plot(distances, marker='o')
plt.title('Distances Between Clicked Points')
plt.xlabel('Measurement Index')
plt.ylabel('Distance (mm)')
plt.grid(True)
# Grafik dosya adı ve yolu oluştur
plot_filename = 'distances_plot.png'
plot_filepath = os.path.join(folder_name, plot_filename)
plt.savefig(plot_filepath)
plt.show()
