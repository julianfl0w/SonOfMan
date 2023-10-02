import cv2
import requests

url = 'http://localhost:8080/video_feed'

# Open the stream using OpenCV
cap = cv2.VideoCapture(url)

frame_counter = 0
while True:
    # Read a frame
    ret, frame = cap.read()
    
    # If the frame was successfully read
    if ret:
        frame_counter += 1
        
        # Save the frame as an image
        #filename = f"frame_{frame_counter}.jpg"
        #cv2.imwrite(filename, frame)
        
        # Display the frame (optional)
        cv2.imshow('Stream', frame)
        
        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        print("Failed to retrieve frame")
        break

cap.release()
cv2.destroyAllWindows()
