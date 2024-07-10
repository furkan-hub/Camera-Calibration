import cv2
import numpy as np

def select_roi(image):
    # Pencereyi oluştur ve pencereyi yeniden boyutlandırılabilir yap
    window_name = "Select ROI"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 800, 600)
    
    # Allow user to select ROI on the original image
    r = cv2.selectROI(window_name, image)
    cv2.destroyWindow(window_name)

    return r

# Load the grayscale BMP image
image_path = 'images/test-11.bmp'
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Check if the image was loaded correctly
if image is None:
    print("Error: Image not loaded. Check the file path.")
else:
    # Allow user to select ROI
    roi = select_roi(image)

    # Crop the image to the selected ROI
    x, y, w, h = roi
    roi_image = image[y:y+h, x:x+w]

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(roi_image, (5, 5), 0)

    # Use Canny Edge Detection to find edges
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours in the edge-detected image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create a white image to draw contours
    contour_image = np.ones_like(roi_image) * 255

    # Draw the contours on the white image
    cv2.drawContours(contour_image, contours, -1, (0, 0, 0), 2)

    # Calculate the total length of the edges in pixels
    total_length = 0
    for contour in contours:
        total_length += cv2.arcLength(contour, True)

    print(f"Total edge length in selected ROI: {total_length} pixels")

    # Pencereyi oluştur ve yeniden boyutlandırılabilir yap
    window_name = 'Contours'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 900, 600)

    while True:
        # Display the image with contours
        cv2.imshow(window_name, contour_image)
        
        # Wait for a key press and break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Close all OpenCV windows
    cv2.destroyAllWindows()
