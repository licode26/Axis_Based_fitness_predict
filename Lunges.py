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
opname = "lunges_output.avi"
start_time = time.time()

lunge_counts = []
lunge_times = []

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
            
            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            
            right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

            # Calculate angles for lunges (example logic, adjust as needed)
            angle_left = calculate_angle(left_hip, left_knee, left_ankle)
            angle_right = calculate_angle(right_hip, right_knee, right_ankle)

            if angle_left > 160 and angle_right > 160:  
                stage = "up"
            if angle_left < 90 and angle_right < 90 and stage == "up":  
                stage = "down"
                counter += 1
                lunge_counts.append(counter)
                lunge_times.append(elapsed_time)
               
                if 70 <= angle_left <= 90 and 70 <= angle_right <= 90: 
                    correct_counter += 1
                engine.say(f"Lunge count: {counter}")
                engine.runAndWait()
                print(f"Lunge Counter: {counter}, Correct Lunges: {correct_counter}")
        
        except:
            pass
        
        text = "{}:{}".format("Lunges", counter)
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

engine.say(f"Exercise completed! Lunges: {counter}. Correct Lunges: {correct_counter}. Accuracy: {accuracy:.2f}%. Well done!")
engine.runAndWait()

# Save progress plot
plt.figure()
plt.plot(lunge_times, lunge_counts, marker='o')
plt.title('Lunge Progress Over Time')
plt.xlabel('Time (seconds)')
plt.ylabel('Number of Lunges')
plt.savefig("lunge_progress.png")
plt.show()

# Prepare data for CSV
csv_file = 'lunge_data.csv'

# Print debug information
print("Lunge Times:", lunge_times)
print("Lunge Counts:", lunge_counts)
print("Total Lunges:", counter)
print("Correct Lunges:", correct_counter)
print("Accuracy:", accuracy)

# Append data to CSV file
with open(csv_file, 'a', newline='') as f:
    writer = csv.writer(f)
    if f.tell() == 0:
        writer.writerow(['Time (seconds)', 'Lunge Count', 'Total Lunges', 'Correct Lunges', 'Accuracy (%)'])
    
    for time, count in zip(lunge_times, lunge_counts):
        writer.writerow([time, count, counter, correct_counter, accuracy])

cap.release()
cv2.destroyAllWindows()
