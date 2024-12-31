import cv2
import numpy as np

# Function to detect the flickering dot in the cropped region
def detect_dot(roi, threshold=200):
    """
    Detects if a dot appears in the given region of interest (ROI).
    Args:
    - roi: The cropped region of interest (grayscale image).
    - threshold: The threshold value to decide if the dot is present.

    Returns:
    - True if a dot is detected, False otherwise.
    """
    # Apply a binary threshold to the region of interest (ROI)
    _, thresh = cv2.threshold(roi, threshold, 255, cv2.THRESH_BINARY)

    # Debug: show the thresholded image (helpful for debugging)
    cv2.imshow("Thresholded ROI", thresh)
    
    # Check if the number of white pixels exceeds a certain threshold (indicating the dot is visible)
    pixel_sum = np.sum(thresh)
    print(f"Pixel sum: {pixel_sum}")  # Debug: print the sum of white pixels
    
    if pixel_sum > 1000:  # Adjust this value depending on the size of your dot
        return True
    return False

# Function to decode Morse code from the flickering dot
def decode_morse_from_video(video_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # List to store the decoded Morse code
    morse_code = ""

    # Time duration to detect a "dot" or "dash" in Morse code
    dot_duration_threshold = 100  # milliseconds (max duration for dot)
    dash_duration_threshold = 300  # milliseconds (min duration for dash)
    
    # Variables to track dot timing
    previous_time = None
    dot_start_time = None  # To track the start time of the dot
    last_dot_time = 0  # Store the last time a dot was detected

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Get the frame dimensions
        height, width = frame.shape[:2]

        # Define the center of the frame
        center_x, center_y = width // 2, height // 2
        
        # Define the size of the region around the center (crop size)
        crop_size = 100  # Adjust this depending on the size of the dot
        
        # Crop the center part of the frame (e.g., 100x100 region around the center)
        cropped_frame = frame[center_y - crop_size // 2 : center_y + crop_size // 2,
                              center_x - crop_size // 2 : center_x + crop_size // 2]

        # Convert to grayscale for thresholding
        gray = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)

        # Detect the dot (flickering)
        dot_present = detect_dot(gray)

        current_time = cap.get(cv2.CAP_PROP_POS_MSEC)  # Get current time in milliseconds

        # Debugging output
        print(f"Current time: {current_time}, Dot present: {dot_present}")

        if dot_present:
            if dot_start_time is None:
                dot_start_time = current_time  # Mark the start of the dot
            
        else:
            if dot_start_time is not None:
                dot_duration = current_time - dot_start_time  # Duration the dot was visible
                print(f"Dot duration: {dot_duration} ms")
                
                # If dot duration is within the range for a "dot"
                if dot_duration < dot_duration_threshold:
                    morse_code += "."  # It's a dot
                elif dot_duration >= dash_duration_threshold:
                    morse_code += "-"  # It's a dash
                
                dot_start_time = None  # Reset the dot start time
        
        # Visualize the frame with the detected region (optional)
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close any OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

    return morse_code

# Example usage:
video_path = r"C:\Users\moham\Downloads\orbs_of_light (online-video-cutter.com).mp4"
morse_code = decode_morse_from_video(video_path)
print("Decoded Morse Code:", morse_code)
