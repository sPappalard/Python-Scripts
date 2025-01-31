import random
import cv2
import mediapipe as mp
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import datetime
import numpy as np
from keras.models import load_model
import gdown
import os

class AdvancedDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Multi-Detection System")
        self.root.geometry("1280x920")
        
        # Initialize variables
        self.cap = None
        self.detection_fps = 0
        self.last_frame_time = 0
        
        # Initialize MediaPipe components
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_pose = mp.solutions.pose
        
        # Initialize detectors
        self.setup_detectors()
        
        # Download and load pre-trained models
        self.setup_additional_models()
        
        # Initialize detection counters and statistics
        self.stats = {
            'faces': 0,
            'hands': 0,
            'smiles': 0,
            'total_frames': 0
        }
        
        self.create_gui()
        
    def setup_detectors(self):
        # Face Detection
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=1,
            min_detection_confidence=0.5
        )
        
        # Face Mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=5,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Hands Detection
        self.hands = self.mp_hands.Hands(
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            max_num_hands=4
        )
        
        # Pose Detection
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
    def setup_additional_models(self):
        # Here you would normally download and load pre-trained models
        # For this example, we'll simulate the models
        # In a real application, you would use actual models for gender, age, and emotion detection
        
        self.models_loaded = True
        self.emotion_labels = ['Angry', 'Happy', 'Neutral', 'Sad', 'Surprised']
        self.gender_labels = ['Male', 'Female']
        
    def create_gui(self):
        # Create main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.grid(row=0, column=0, sticky="nsew")
        
        # Create left panel for controls
        self.create_control_panel()
        
        # Create right panel for video and stats
        self.create_video_panel()
        
        # Create bottom panel for detailed stats
        self.create_stats_panel()
        
    def create_control_panel(self):
        control_frame = ttk.LabelFrame(self.main_container, text="Detection Controls", padding="10")
        control_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        # Detection toggles
        self.detection_vars = {
            'face': tk.BooleanVar(value=True),
            'hands': tk.BooleanVar(value=True),
            'pose': tk.BooleanVar(value=False),
            'landmarks': tk.BooleanVar(value=True),
            'gender': tk.BooleanVar(value=True),
            'emotion': tk.BooleanVar(value=True),
            'age': tk.BooleanVar(value=True)
        }
        
        row = 0
        for name, var in self.detection_vars.items():
            ttk.Checkbutton(
                control_frame,
                text=f"Enable {name.title()} Detection",
                variable=var
            ).grid(row=row, column=0, pady=2, sticky="w")
            row += 1
        
        # Confidence threshold controls
        ttk.Label(control_frame, text="Detection Confidence:").grid(row=row, column=0, pady=5)
        self.confidence_var = tk.DoubleVar(value=0.5)
        confidence_slider = ttk.Scale(
            control_frame,
            from_=0.1,
            to=1.0,
            variable=self.confidence_var,
            orient=tk.HORIZONTAL
        )
        confidence_slider.grid(row=row+1, column=0, sticky="ew")
        
        # Camera controls
        camera_frame = ttk.LabelFrame(control_frame, text="Camera Controls", padding="5")
        camera_frame.grid(row=row+2, column=0, pady=10, sticky="ew")
        
        ttk.Button(
            camera_frame,
            text="Start Camera",
            command=self.start_webcam
        ).grid(row=0, column=0, padx=5)
        
        ttk.Button(
            camera_frame,
            text="Stop Camera",
            command=self.stop_webcam
        ).grid(row=0, column=1, padx=5)
        
        # Screenshot button
        ttk.Button(
            control_frame,
            text="Take Screenshot",
            command=self.take_screenshot
        ).grid(row=row+3, column=0, pady=10)
        
    def create_video_panel(self):
        video_frame = ttk.LabelFrame(self.main_container, text="Video Feed", padding="5")
        video_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        self.video_label = ttk.Label(video_frame)
        self.video_label.grid(row=0, column=0)
        
        # FPS counter
        self.fps_var = tk.StringVar(value="FPS: 0")
        ttk.Label(
            video_frame,
            textvariable=self.fps_var
        ).grid(row=1, column=0)
        
    def create_stats_panel(self):
        stats_frame = ttk.LabelFrame(self.main_container, text="Detection Statistics", padding="5")
        stats_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        
        # Create variables for statistics
        self.stats_vars = {
            'Faces Detected': tk.StringVar(value="0"),
            'Hands Detected': tk.StringVar(value="0"),
            'Smiles Detected': tk.StringVar(value="0"),
            'Current Emotion': tk.StringVar(value="N/A"),
            'Estimated Age': tk.StringVar(value="N/A"),
            'Detected Gender': tk.StringVar(value="N/A")
        }
        
        col = 0
        for label, var in self.stats_vars.items():
            ttk.Label(stats_frame, text=f"{label}:").grid(row=0, column=col*2, padx=5)
            ttk.Label(stats_frame, textvariable=var).grid(row=0, column=col*2+1, padx=5)
            col += 1
    # Add this method to the AdvancedDetectionApp class
    def process_facial_features(self, frame, detection):
        """Process facial features including landmarks, emotion, and expressions"""
        try:
            # Get face bounding box
            bbox = detection.location_data.relative_bounding_box
            h, w, _ = frame.shape
            x = int(bbox.xmin * w)
            y = int(bbox.ymin * h)
            width = int(bbox.width * w)
            height = int(bbox.height * h)
            
            # Extract face ROI
            face_roi = frame[y:y+height, x:x+width]
            if face_roi.size == 0:
                return

            # Process facial landmarks if enabled
            if self.detection_vars['landmarks'].get():
                # Convert ROI to RGB for MediaPipe
                roi_rgb = cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB)
                mesh_results = self.face_mesh.process(roi_rgb)
                
                if mesh_results.multi_face_landmarks:
                    for face_landmarks in mesh_results.multi_face_landmarks:
                        # Adjust landmark coordinates to face ROI
                        for landmark in face_landmarks.landmark:
                            landmark_x = int(landmark.x * width) + x
                            landmark_y = int(landmark.y * height) + y
                            cv2.circle(frame, (landmark_x, landmark_y), 1, (0, 255, 0), -1)

            # Simulate emotion detection
            if self.detection_vars['emotion'].get():
                emotion = np.random.choice(self.emotion_labels)
                cv2.putText(frame, f"Emotion: {emotion}", 
                        (x, y + height + 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

            # Simulate smile detection
            if random.random() > 0.5:  # Simulate smile detection
                cv2.putText(frame, "Smiling", 
                        (x, y + height + 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                self.stats['smiles'] += 1

        except Exception as e:
            print(f"Error in process_facial_features: {str(e)}")

    # Also modify the process_frame method to include better error handling:
    def process_frame(self, frame):
        try:
            if frame is None:
                return frame
                
            # Convert to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = {'faces': 0, 'hands': 0, 'smiles': 0}
            
            # Process faces
            if self.detection_vars['face'].get():
                face_results = self.face_detection.process(rgb_frame)
                if face_results.detections:
                    results['faces'] = len(face_results.detections)
                    for detection in face_results.detections:
                        if detection.score[0] > self.confidence_var.get():
                            self.draw_face_detection(frame, detection)
                            
                            # Process facial features if enabled
                            if self.detection_vars['landmarks'].get():
                                self.process_facial_features(frame, detection)
            
            # Process hands
            if self.detection_vars['hands'].get():
                hands_results = self.hands.process(rgb_frame)
                if hands_results.multi_hand_landmarks:
                    results['hands'] = len(hands_results.multi_hand_landmarks)
                    self.draw_hands(frame, hands_results)
            
            # Process pose
            if self.detection_vars['pose'].get():
                pose_results = self.pose.process(rgb_frame)
                if pose_results.pose_landmarks:
                    self.draw_pose(frame, pose_results)
            
            # Update statistics
            self.update_statistics(results)
            
            # Calculate and display FPS
            self.calculate_fps()
            
            return frame

        except Exception as e:
            print(f"Error in process_frame: {str(e)}")
            return frame

    
    
    def draw_face_detection(self, frame, detection):
        bbox = detection.location_data.relative_bounding_box
        h, w, _ = frame.shape
        x = int(bbox.xmin * w)
        y = int(bbox.ymin * h)
        width = int(bbox.width * w)
        height = int(bbox.height * h)
        
        # Draw face rectangle
        cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)
        
        # Draw confidence score
        confidence = f'{int(detection.score[0] * 100)}%'
        cv2.putText(frame, confidence, (x, y - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Simulate gender and age detection
        if self.detection_vars['gender'].get():
            gender = np.random.choice(self.gender_labels)
            self.stats_vars['Detected Gender'].set(gender)
            cv2.putText(frame, f"Gender: {gender}", (x, y + height + 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        
        if self.detection_vars['age'].get():
            age = np.random.randint(15, 70)
            self.stats_vars['Estimated Age'].set(str(age))
            cv2.putText(frame, f"Age: {age}", (x, y + height + 40),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
    
    def draw_hands(self, frame, results):
        for hand_landmarks in results.multi_hand_landmarks:
            self.mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                self.mp_hands.HAND_CONNECTIONS,
                self.mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=2),
                self.mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2)
            )
    
    def draw_pose(self, frame, results):
        self.mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            self.mp_pose.POSE_CONNECTIONS,
            self.mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2),
            self.mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2)
        )
    
    def calculate_fps(self):
        current_time = cv2.getTickCount()
        if self.last_frame_time:
            self.detection_fps = cv2.getTickFrequency() / (current_time - self.last_frame_time)
        self.last_frame_time = current_time
        self.fps_var.set(f"FPS: {self.detection_fps:.1f}")
    
    def update_statistics(self, results):
        for key, value in results.items():
            if key in self.stats:
                self.stats[key] = value
        
        self.stats_vars['Faces Detected'].set(str(self.stats['faces']))
        self.stats_vars['Hands Detected'].set(str(self.stats['hands']))
        self.stats_vars['Smiles Detected'].set(str(self.stats['smiles']))
        
        # Simulate emotion detection
        if self.stats['faces'] > 0 and self.detection_vars['emotion'].get():
            emotion = np.random.choice(self.emotion_labels)
            self.stats_vars['Current Emotion'].set(emotion)
    
    def take_screenshot(self):
        if hasattr(self, 'current_frame'):
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"detection_screenshot_{timestamp}.jpg"
            cv2.imwrite(filename, self.current_frame)
            messagebox.showinfo("Screenshot", f"Screenshot saved as {filename}")
    
    def start_webcam(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("Error", "Could not open webcam!")
                return
            
            # Set higher resolution
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            
            self.update_frame()
    
    def stop_webcam(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
            self.video_label.configure(image='')
    
    def update_frame(self):
        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                self.current_frame = frame.copy()
                
                # Process the frame
                processed_frame = self.process_frame(frame)
                
                # Convert to PhotoImage for display
                frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                display_size = (800, 600)
                img = img.resize(display_size, Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image=img)
                
                self.video_label.configure(image=photo)
                self.video_label.image = photo
            
            self.root.after(10, self.update_frame)
    
    def __del__(self):
        if self.cap is not None:
            self.cap.release()

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedDetectionApp(root)
    root.mainloop()