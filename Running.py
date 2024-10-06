import cv2
import mediapipe as mp
import numpy as np
import time
import pyttsx3
import matplotlib.pyplot as plt
import csv

def calculate_distance(p1, p2):
    return np.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

engine = pyttsx3.init()

start_time = time.time()
last_position = None
total_distance = 0
distances = []
times = []

cap = cv2.VideoCapture(0)

with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        elapsed_time = time.time() - start_time
        if elapsed_time > 30:
            break  
        
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
      
        results = pose.process(image)
    
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        try:
            landmarks = results.pose_landmarks.landmark
            
            # Use left ankle for distance calculation
            left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            
            if last_position is not None:
                distance = calculate_distance(last_position, left_ankle)
                total_distance += distance
                distances.append(total_distance)
                times.append(elapsed_time)
                
            last_position = left_ankle
            
            engine.say(f"Total distance covered: {total_distance:.2f} meters")
            engine.runAndWait()
            print(f"Elapsed Time: {elapsed_time:.2f} seconds, Total Distance: {total_distance:.2f} meters")
        
        except:
            pass
        
        text = "{}: {:.2f} meters".format("Distance", total_distance)
        cv2.putText(image, text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))               

        cv2.imshow('Mediapipe Feed', image)

        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

# Save progress plot
plt.figure()
plt.plot(times, distances, marker='o')
plt.title('Running Distance Over Time')
plt.xlabel('Time (seconds)')
plt.ylabel('Distance (meters)')
plt.savefig("running_progress.png")
plt.show()

# Prepare data for CSV
csv_file = 'running_data.csv'

# Print debug information
print("Times:", times)
print("Distances:", distances)
print("Total Distance:", total_distance)

# Append data to CSV file
with open(csv_file, 'a', newline='') as f:
    writer = csv.writer(f)
    if f.tell() == 0:
        writer.writerow(['Time (seconds)', 'Total Distance (meters)'])
    
    for time, distance in zip(times, distances):
        writer.writerow([time, distance])
