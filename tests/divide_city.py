'''Test workspace to try and split a city image into tile images'''
import cv2

# Load the image (provide the correct path)
image = cv2.imread("images/image.jpg")

# Check if the image was loaded successfully
if image is None:
    print("Error: Could not load image.")
else:
    # Display the image
    cv2.imshow("Loaded Image", image)
    
    # Wait for a key press and close the window
    cv2.waitKey(0)
    cv2.destroyAllWindows()









if __name__ == "__main__":
    
    pass