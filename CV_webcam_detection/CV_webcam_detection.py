import cv2
import os
import tkinter as tk
from tkinter import messagebox

# paths to xml files containing the pre-trained face and smile detection templates.
face_cascade_path = 'classifiers/haarcascade_frontalface_default.xml'
smile_cascade_path = 'classifiers/haarcascade_smile.xml'

# Check that the files exist in the specified location
if not os.path.exists(face_cascade_path):
    print(f"Error: The file {face_cascade_path} was not found.")
if not os.path.exists(smile_cascade_path):
    print(f"Error: The file {smile_cascade_path} was not found.")


# Loading of the classifiers
face_cascade = cv2.CascadeClassifier(face_cascade_path)
smile_cascade = cv2.CascadeClassifier(smile_cascade_path)

# Check that the folders have been loaded correctly
if face_cascade.empty():
    print("Error: The file haarcascade_frontalface_default.xml was not loaded correctly.")
else:
    print("Face classifier file loaded correctly.")

if smile_cascade.empty():
    print("Error: The haarcascade_smile.xml file was not loaded correctly.")
else:
    print("Smile classifier file loaded correctly.")

# Smile detection function
def detect_smile():
    # Start of the webcam
    cap = cv2.VideoCapture(0)       #The argument '0' indicates the default webcam on your computer.

    # A while cycle continues to read frames from the webcam until it is stopped
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        #Converts any frame from color (BGR) to grayscale--> Black and white conversion makes it easy to detect faces and smiles.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Face detection
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))       #the parameters: scaleFactor: Check the image size during detection (1.1 is a typical value). |  minNeighbors: Specifies how many neighbors of a window must be considered to determine if there is a face. | minSize: The minimum size of the face to be detected.

        if len(faces) == 0:
            cv2.putText(frame, "I don't see anybody", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            # For each face found
            for (x, y, w, h) in faces:
                # Draw the rectangle around the face
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Smile detection inside the face
                #Within the detected face, we take the region of interest (ROI) and look for the smile in that part of the image (to reduce the number of false positives).
                roi_gray = gray[y:y + h, x:x + w]
                smiles = smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.8, minNeighbors=20, minSize=(25, 25))

                if len(smiles) > 0:
                    cv2.putText(frame, "You're smiling!", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                else:
                    cv2.putText(frame, "You are not smiling", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Show the frame with the face and smile (or lack of smile) in the "Smile Detection" window.
        cv2.imshow("Smile Detection", frame)

        # Exit if the user presses 'q
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            

    # Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()

#  main menu
def show_main_menu():
    def start_smile_detection():
        root.withdraw()  # Hide the main window
        detect_smile()

    # Creation of main window
    root = tk.Tk()
    root.title("My first detection Tool!")
    root.geometry("400x300")
    root.config(bg="#f0f0f0")  

    title_label = tk.Label(root, text="Welcome to my first detection tool!", font=("Arial", 14), bg="#f0f0f0")
    title_label.pack(pady=20)

    description_label = tk.Label(root, text="Select the mode:", font=("Arial", 12), bg="#f0f0f0")
    description_label.pack(pady=10)

    # Button for Smile Detection
    smile_button = tk.Button(root, text="Start Smile Detection", font=("Arial", 12), bg="#4CAF50", fg="white", command=start_smile_detection, padx=10, pady=5)
    smile_button.pack(pady=20)

    quit_button = tk.Button(root, text="Exit", font=("Arial", 12), bg="#f44336", fg="white", command=root.quit, padx=10, pady=5)
    quit_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    show_main_menu()
