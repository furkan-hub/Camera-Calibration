import cv2
import numpy as np

def select_roi(image):
    # Resize image for ROI selection to fit the screen
    scale_percent = 30  # Percentage of original size
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    resized_image = cv2.resize(image, (width, height))

    # Allow user to select ROI on the resized image
    r = cv2.selectROI("Select ROI", resized_image)
    cv2.destroyWindow("Select ROI")

    # Scale the ROI back to the original image size
    r = (int(r[0] * 100 / scale_percent), int(r[1] * 100 / scale_percent), int(r[2] * 100 / scale_percent), int(r[3] * 100 / scale_percent))
    return r

# Load the grayscale BMP image
image_path = 'test.bmp'
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

    # Loop through each contour to calculate its bounding box size and draw it
    for contour in contours:
        x_contour, y_contour, w_contour, h_contour = cv2.boundingRect(contour)
        cv2.rectangle(contour_image, (x_contour, y_contour), (x_contour + w_contour, y_contour + h_contour), (0, 255, 0), 2)
        
        # Only write the width and height if both are 150 pixels or larger
        if w_contour >= 150 and h_contour >= 150:
            text = f"{w_contour}x{h_contour}"
            font_scale = 1
            font_thickness = 1
            text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)
            text_x = x_contour + (w_contour - text_size[0]) // 2
            text_y = y_contour + (h_contour + text_size[1]) // 2
            cv2.putText(contour_image, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 255), font_thickness)

    # Resize the image for display
    resized_image = cv2.resize(contour_image, (900, 600))

    while True:
        # Display the image with contours and sizes
        cv2.imshow('Contours', resized_image)
        
        # Wait for a key press and break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Close all OpenCV windows
    cv2.destroyAllWindows()
