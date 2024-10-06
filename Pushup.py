import cv2
import mediapipe as mp
import numpy as np
import time
import pyttsx3
import matplotlib.pyplot as plt
import csv

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(np.degrees(radians))
    
    if angle > 180.0:
        angle = 360 - angle
        
    return angle 

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

engine = pyttsx3.init()

counter = 0
correct_counter = 0
stage = None
create = None
opname = "pushup_output.avi"
start_time = time.time()

pushup_counts = []
pushup_times = []

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
            
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

            angle_left = calculate_angle(left_shoulder, left_elbow, left_wrist)
            angle_right = calculate_angle(right_shoulder, right_elbow, right_wrist)

            if angle_left > 160 and angle_right > 160:  
                stage = "up"
            if angle_left < 90 and angle_right < 90 and stage == "up":  
                stage = "down"
                counter += 1
                pushup_counts.append(counter)
                pushup_times.append(elapsed_time)
               
                if 70 <= angle_left <= 90 and 70 <= angle_right <= 90: 
                    correct_counter += 1
                engine.say(f"Push-up count: {counter}")
                engine.runAndWait()
                print(f"Push-Up Counter: {counter}, Correct Push-Ups: {correct_counter}")
        
        except:
            pass
        
        text = "{}:{}".format("Push-Ups", counter)
        cv2.putText(image, text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))               

        cv2.imshow('Mediapipe Feed', image)

        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break

        if create is None:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            create = cv2.VideoWriter(opname, fourcc, 30, (image.shape[1], image.shape[0]), True)
        create.write(image)

accuracy = (correct_counter / counter) * 100 if counter > 0 else 0

engine.say(f"Exercise completed! Push-Ups: {counter}. Correct Push-Ups: {correct_counter}. Accuracy: {accuracy:.2f}%. Well done!")
engine.runAndWait()

# Save progress plot
plt.figure()
plt.plot(pushup_times, pushup_counts, marker='o')
plt.title('Push-Up Progress Over Time')
plt.xlabel('Time (seconds)')
plt.ylabel('Number of Push-Ups')
plt.savefig("pushup_progress.png")
plt.show()

# Prepare data for CSV
csv_file = 'pushup_data.csv'

# Print debug information
print("Push-Up Times:", pushup_times)
print("Push-Up Counts:", pushup_counts)
print("Total Push-Ups:", counter)
print("Correct Push-Ups:", correct_counter)
print("Accuracy:", accuracy)

# Append data to CSV file
with open(csv_file, 'a', newline='') as f:
    writer = csv.writer(f)
    if f.tell() == 0:
        writer.writerow(['Time (seconds)', 'Push-Up Count', 'Total Push-Ups', 'Correct Push-Ups', 'Accuracy (%)'])
    
    for time, count in zip(pushup_times, pushup_counts):
        writer.writerow([time, count, counter, correct_counter, accuracy])

cap.release()
cv2.destroyAllWindows()
