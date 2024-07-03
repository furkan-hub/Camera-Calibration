
import cv2
import pickle
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Load calibration data
with open(r'C:\Users\Gedik\Desktop\ComputerVision\calibration_data.pkl', 'rb') as f:
    mtx, dist = pickle.load(f)

# Open the video capture
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 4656)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 3496)
cap.set(cv2.CAP_PROP_FPS, 1)

def take_photo():
    ret, frame = cap.read()
    if ret:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        photo_filename = f'captured_photo_{timestamp}.png'
        undistorted_frame = cv2.undistort(frame, mtx, dist, None, mtx)
        blur= cv2.blur(undistorted_frame,(5,5))
        cv2.imwrite(photo_filename, blur)
        messagebox.showinfo("Photo Capture", f"Photo saved as {photo_filename}")
    else:
        messagebox.showerror("Photo Capture", "Failed to capture photo")

root = tk.Tk()
root.title("Photo Capture")

capture_button = tk.Button(root, text="Take Photo", command=take_photo)
capture_button.pack(pady=20)

def show_frame():
    ret, frame = cap.read()
    if ret:
        height, width, channels = frame.shape
        x_center = width // 2
        y_center = height // 2
        half_crop_size = 500 // 2
        
        cropped_image = frame[y_center-half_crop_size:y_center+half_crop_size, x_center-half_crop_size:x_center+half_crop_size]
        cropped_image2=frame[0:500,0:500]
        
        undistorted_frame = cv2.undistort(frame, mtx, dist, None, mtx)
        blur= cv2.blur(undistorted_frame,(5,5))
        # cv2.imshow("Cropped Image", cv2.resize(cropped_image, (800, 800)))
        # cv2.imshow("Cropped Edge",cv2.resize(cropped_image2,(800,800)))
        # cv2.imshow("Original", cv2.resize(frame, (800, 800)))
        cv2.imshow("Undistorted", cv2.resize(blur, (800, 800)))
        
    root.after(10, show_frame)

def on_closing():
    cap.release()
    cv2.destroyAllWindows()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

show_frame()
root.mainloop()
