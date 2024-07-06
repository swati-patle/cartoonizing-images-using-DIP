# -*- coding: utf-8 -*-
import cv2
import os
import time

class Cartoonizer:
    def __init__(self):
        pass

    def cartoonize_frame(self, frame):
        # Number of downscaling steps
        num_down_samples = 2
        
        # Number of bilateral filtering steps
        num_bilateral_filters = 20
        
        # -- STEP 1: Downsample using Gaussian pyramid --
        img_color = frame
        for _ in range(num_down_samples):
            img_color = cv2.pyrDown(img_color)
        
        # -- STEP 2: Apply bilateral filtering --
        for _ in range(num_bilateral_filters):
            img_color = cv2.bilateralFilter(img_color, 9, 9, 7)
        
        # -- STEP 3: Upsample to original size --
        for _ in range(num_down_samples):
            img_color = cv2.pyrUp(img_color)
        
        # -- STEP 4: Convert to grayscale and apply median blur --
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img_blur = cv2.medianBlur(img_gray, 3)
        
        # -- STEP 5: Detect and enhance edges --
        img_edge = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)
        
        # -- STEP 6: Convert edge-detected image back to color --
        (x, y, z) = img_color.shape
        img_edge = cv2.resize(img_edge, (y, x))
        img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)
        
        # -- STEP 7: Combine color image with edge-detected image using bitwise AND --
        cartoonized_frame = cv2.bitwise_and(img_color, img_edge)
        
        return cartoonized_frame

# Cartoonize image
def cartoonize_image(input_image_path, output_image_path):
    cartoonizer = Cartoonizer()
    # Read input image
    for i, input_image_path in enumerate(input_image_path):
        # Read input image
        img_rgb = cv2.imread(input_image_path)
        
        # Cartoonize image
        cartoonized_image = cartoonizer.cartoonize_frame(img_rgb)
        cv2.imshow(f"Cartoonized Image {i+1}", cartoonized_image)
        
        
        # # Move the window to the top-left corner
        cv2.moveWindow(f"Cartoonized Image {i+1}", 0, 0) 
        
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        # Save cartoonized image
        output_image_path = (f"{output_image_path}/cartoonized_images_{i}.jpg")
        cv2.imwrite(output_image_path, cartoonized_image)
        
        print(f"Cartoonized image {i} saved as: {output_image_path}")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
def blink_images(image_paths, delay=0.1):
    for path in image_paths:
        if os.path.exists(path):  # Check if file exists
            img = cv2.imread(path)
            if img is not None:  # Check if image loaded successfully
                cv2.imshow('Image', img)
                cv2.waitKey(1)
                time.sleep(delay)
                cv2.destroyAllWindows()  # Close the window after displaying the image
                time.sleep(delay)  # Wait for a short duration before displaying the next image
            else:
                print(f"Error: Unable to load image '{path}'")
        else:
            print(f"Error: Image file '{path}' not found")

 
input_image_path = [r"C:\Users\Swati Patle\Desktop\sAMPLE aNIMATION\app1.jpg", r"C:\Users\Swati Patle\Desktop\sAMPLE aNIMATION\app2.jpg", r"C:\Users\Swati Patle\Desktop\sAMPLE aNIMATION\app3.jpg",r"C:\Users\Swati Patle\Desktop\sAMPLE aNIMATION\app4.jpg",r"C:\Users\Swati Patle\Desktop\sAMPLE aNIMATION\app5.jpg",r"C:\Users\Swati Patle\Desktop\sAMPLE aNIMATION\app6.jpg",r"C:\Users\Swati Patle\Desktop\sAMPLE aNIMATION\app7.jpg",r"C:\Users\Swati Patle\Desktop\sAMPLE aNIMATION\app8.jpg",r"C:\Users\Swati Patle\Desktop\sAMPLE aNIMATION\app9.jpg",r"C:\Users\Swati Patle\Desktop\sAMPLE aNIMATION\app10.jpg",r"C:\Users\Swati Patle\Desktop\sAMPLE aNIMATION\app11.jpg",r"C:\Users\Swati Patle\Desktop\sAMPLE aNIMATION\app12.jpg",r"C:\Users\Swati Patle\Desktop\sAMPLE aNIMATION\app13.jpg",r"C:\Users\Swati Patle\Desktop\sAMPLE aNIMATION\app14.jpg",r"C:\Users\Swati Patle\Desktop\sAMPLE aNIMATION\app15 .jpg"]
output_image_path = "cartoonized_images"
cartoonize_image(input_image_path, output_image_path)
image_files = [os.path.join(input_image_path, file) for file in os.listdir(input_image_path) if file.endswith(('jpg', 'jpeg', 'png'))]
blink_images(image_files)