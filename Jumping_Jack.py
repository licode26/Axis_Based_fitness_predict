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
opname = "jumping_jacks_output.avi"
start_time = time.time()

jack_counts = []
jack_times = []

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

            shoulder_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
            elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

            # Detect jumping jacks by looking for distinct movements
            if shoulder_angle < 30 and elbow_angle < 30:
                stage = "up"
            if shoulder_angle > 60 and elbow_angle > 60 and stage == "up":
                stage = "down"
                counter += 1
                jack_counts.append(counter)
                jack_times.append(elapsed_time)
                
                engine.say(f"Jumping Jack count: {counter}")
                engine.runAndWait()
                print(f"Jumping Jack Counter: {counter}")
        
        except:
            pass
        
        text = "{}:{}".format("Jumping Jacks", counter)
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

engine.say(f"Exercise completed! Jumping Jacks: {counter}. Correct Jumping Jacks: {correct_counter}. Accuracy: {accuracy:.2f}%. Well done!")
engine.runAndWait()

# Save progress plot
plt.figure()
plt.plot(jack_times, jack_counts, marker='o')
plt.title('Jumping Jack Progress Over Time')
plt.xlabel('Time (seconds)')
plt.ylabel('Number of Jumping Jacks')
plt.savefig("jumping_jack_progress.png")
plt.show()

# Prepare data for CSV
csv_file = 'jumping_jack_data.csv'

# Print debug information
print("Jumping Jack Times:", jack_times)
print("Jumping Jack Counts:", jack_counts)
print("Total Jumping Jacks:", counter)
print("Correct Jumping Jacks:", correct_counter)
print("Accuracy:", accuracy)

# Append data to CSV file
with open(csv_file, 'a', newline='') as f:
    writer = csv.writer(f)
    if f.tell() == 0:
        writer.writerow(['Time (seconds)', 'Jumping Jack Count', 'Total Jumping Jacks', 'Correct Jumping Jacks', 'Accuracy (%)'])
    
    for time, count in zip(jack_times, jack_counts):
        writer.writerow([time, count, counter, correct_counter, accuracy])

cap.release()
cv2.destroyAllWindows()
