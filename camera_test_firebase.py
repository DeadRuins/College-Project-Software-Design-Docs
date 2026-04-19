import cv2
import time
import os
import firebase_admin
from firebase_admin import credentials, storage

class VideoHandler:
    def __init__(self):
        #Firebase rubbish
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred, {
            'storageBucket': 'camera-project-22d9a.firebasestorage.app'
        })
        self.bucket = storage.bucket()

        # Initialize the camera inside the class
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

        if not os.path.exists("captures"):
            os.makedirs("captures")

    def upload_to_firebase(self, file_path, remote_name):
        blob = self.bucket.blob(remote_name)
        blob.upload_from_filename(file_path)
        print(f"Uploaded {remote_name} to Firebase!")

    def run(self):
        last_save_time = time.time()
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            cv2.imshow("Frame", frame)

            # Check current time
            current_time = time.time()

            # If 10 seconds have passed
            if current_time - last_save_time >= 10:
                # Generate a filename based on the timestamp
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                filename = "latest_capture.webp"

                # Save the image (WebP format)
                # You can adjust quality from 1-100; default is 80
                cv2.imwrite(filename, frame, [cv2.IMWRITE_WEBP_QUALITY, 80])
                print(f"Saved: {filename}")

                self.upload_to_firebase(filename, "current_view.webp")

                last_save_time = current_time

            # Wait for 1ms and check if Esc (27) is pressed
            if cv2.waitKey(1) == 27:
              break

        # Cleanup
        self.cap.release()
        cv2.destroyAllWindows()

# To use the class:
if __name__ == "__main__":
    app = VideoHandler()
    app.run()
