import cv2  # Library for image processing
import numpy as np  # Library for working with arrays and matrices

def load_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Unable to load image from '{}'".format(image_path))
        exit()
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyWindow('image')
    return image


def detection_maze(image, scale):
    # Resize the image based on the scale
    height, width = image.shape[:2]
    resized_image = cv2.resize(image, (int(width * scale), int(height * scale)))

    # Convert the image to grayscale
    gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Gray", gray)
    cv2.waitKey(0)

    # Apply a Gaussian blur to reduce noise
    blurred_gray = cv2.GaussianBlur(gray, (5, 5), 0)

    cv2.imshow("Blurred Gray", blurred_gray)
    cv2.waitKey(0)

    # Detect edges using Canny Edge Detection
    edges = cv2.Canny(blurred_gray, threshold1=50, threshold2=200)
    cv2.imshow("Edges", edges)
    cv2.waitKey(0)

    # Apply morphological filters to enhance edges
    kernel = np.ones((5, 5), np.uint8)
    enhanced_edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    # Find contours in the image
    contours, _ = cv2.findContours(enhanced_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours to find those that might represent a maze
    best_contour = None
    best_area = 0

    for contour in contours:
        # Calculate the area of the contour
        area = cv2.contourArea(contour)

        # Ignore contours that are too small (adjust threshold based on scale)
        if area < 500 / scale:  # <<< THRESHOLD SCALED BASED ON SIZE
            continue

        # Get the bounding rectangle of the contour
        x, y, w, h = cv2.boundingRect(contour)

        # Calculate the aspect ratio (width/height)
        aspect_ratio = w / h

        # Ignore contours with extreme aspect ratios (e.g., thin lines)
        if aspect_ratio < 0.3 or aspect_ratio > 3:
            continue

        # Save the contour with the largest area (presumably the maze)
        if area > best_area:
            best_area = area
            best_contour = contour

    return best_contour, scale


def main():
    img = load_image('./maze_image/boh1.png')

    scales = [1.0, 1.5, 2.0, 0.75, 0.5]  # Different scales to test
    best_contour = None
    best_scale = 1.0
    best_area = 0

    for scale in scales:
        contour, scale_used = detection_maze(img, scale)
        if contour is not None:
            area = cv2.contourArea(contour)
            if area > best_area:
                best_area = area
                best_contour = contour
                best_scale = scale_used

    if best_contour is None:
        print("Error: No maze detected.")
        exit()

    # 3. Resize the final image based on the best scale found
    height, width = img.shape[:2]
    resized_image = cv2.resize(img, (int(width * best_scale), int(height * best_scale)))

    # Draw the best contour found on the resized image
    image_with_best_contour = resized_image.copy()
    cv2.drawContours(image_with_best_contour, [best_contour], -1, (255, 0, 0), 2)
    cv2.imshow("Best Contour", image_with_best_contour)
    cv2.waitKey(0)

    # 4. Get the bounding rectangle of the maze
    x, y, w, h = cv2.boundingRect(best_contour)

    # Draw the bounding rectangle on the original image for verification
    image_with_rectangle = resized_image.copy()
    cv2.rectangle(image_with_rectangle, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2.imshow("Bounding Rectangle", image_with_rectangle)
    cv2.waitKey(0)

    # 5. Crop the maze from the original image
    cropped_maze = resized_image[y:y + h, x:x + w]

    # Show the cropped maze
    cv2.imshow("Cropped Maze", cropped_maze)
    cv2.waitKey(0)

    # Save the cropped image
    cv2.imwrite("cropped_maze.png", cropped_maze)

    # Close all windows
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
