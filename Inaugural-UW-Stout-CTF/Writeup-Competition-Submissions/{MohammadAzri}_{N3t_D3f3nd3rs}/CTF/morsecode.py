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

    # Check if the number of white pixels exceeds a certain threshold (indicating the dot is visible)
    pixel_sum = np.sum(thresh)
    
    if pixel_sum > 5000:  # Adjust this value depending on the size of your dot
        return True
    return False

# Function to decode Morse code from the flickering dot in the video file
def decode_morse_from_video(video_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # List to store the decoded Morse code
    morse_code = ""

    # Capture the first frame to get the frame rate (FPS)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"Frames per second (FPS): {fps}")

    # Get the frame dimensions
    ret, frame = cap.read()
    height, width = frame.shape[:2]

    # Variables to track timing for dots, dashes, and spaces
    dot_time_threshold = 300  # Time threshold (milliseconds) to detect a dot
    dash_time_threshold = 600  # Time threshold (milliseconds) to detect a dash
    letter_time_threshold = 700  # Time threshold (milliseconds) to detect space between letters
    word_time_threshold = 1500  # Time threshold (milliseconds) to detect space between words
    last_dot_time = None  # To store the time of the last dot detected
    last_flicker_time = 0  # Last flicker time

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

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
        print(f"Current time: {current_time} ms, Dot present: {dot_present}")

        if dot_present:
            if last_dot_time is None or current_time - last_dot_time > dot_time_threshold:
                morse_code += "."  # Add dot to Morse code if dot is present
            last_dot_time = current_time  # Update last dot time
        else:
            if last_dot_time is not None:
                gap_time = current_time - last_dot_time

                # Handle space between dots/dashes or words
                if gap_time > word_time_threshold:
                    morse_code += " / "  # Space between words (use "/" for word separator)
                elif gap_time > letter_time_threshold:
                    morse_code += " "  # Space between letters

                # Check if gap_time is larger than dash_time_threshold to indicate a dash
                if gap_time > dash_time_threshold:
                    morse_code += "-"  # Add dash to Morse code

        # Show the current frame with the detected region (optional)
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close any OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

    # Filter out any invalid Morse code characters (only dots, dashes, spaces, and slashes)
    valid_morse_code = ''.join(c for c in morse_code if c in ['.', '-', ' ', '/'])

    return valid_morse_code

# Example usage:
video_path = r"C:\Users\moham\Downloads\output_video.mp4"  # Path to the saved video file
morse_code = decode_morse_from_video(video_path)
print("Decoded Morse Code:", morse_code)
