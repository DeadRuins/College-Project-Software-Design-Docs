import cv2
import time
import threading
import uvicorn
import pygame
from fastapi import FastAPI, Response
from fastapi.responses import FileResponse, HTMLResponse

app = FastAPI()
latest_frame = None

ALARM_PATH = "alarm.ogg"

@app.post("/trigger-alarm")
async def trigger_alarm():
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(ALARM_PATH)
        pygame.mixer.music.play()
        print("Alarm Triggered!")
        return {"status": "success", "message": "Alarm is playing"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# This route serves the image to your phone
@app.get("/", response_class=HTMLResponse)
async def index():
    html_content = """
    <html>
        <head>
            <title>Security Camera</title>
            <script>
                async function soundAlarm() {
                    const btn = document.getElementById('alarmBtn');
                    btn.disabled = true;
                    btn.innerText = 'Ringing...';

                    await fetch('/trigger-alarm', { method: 'POST' });

                    setTimeout(() => {
                        btn.disabled = false;
                        btn.innerText = 'TRIGGER ALARM';
                    }, 3000);
                }

                document.getElementById('time').innerHTML = new Date().toLocaleTimeString();
            </script>

        </head>
        <body style="background: #222; color: white; text-align: center; font-family: sans-serif;">
            <h1>Live Feed (updates every 10s)</h1>
            <img src="/latest" style="max-width: 90%; border: 5px solid #444;">
            <p>Last refresh: <span id="time"></span></p>

            <button id="alarmBtn" onclick="soundAlarm()"
                style="padding: 20px 40px; font-size: 24px; background: red; color: white; border: none; border-radius: 10px; cursor: pointer;">
                TRIGGER ALARM
            </button>

        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/latest")
async def get_latest():
    return FileResponse("current_view.webp", media_type="image/webp")

class VideoHandler:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

    def run_camera(self):
        last_save_time = time.time()
        while True:
            ret, frame = self.cap.read()
            if not ret: break

            cv2.imshow("Frame", frame)

            if time.time() - last_save_time >= 10:
                cv2.imwrite("current_view.webp", frame, [cv2.IMWRITE_WEBP_QUALITY, 80])
                last_save_time = time.time()
                print("Image updated on server.")

            if cv2.waitKey(1) == 27: break

        self.cap.release()
        cv2.destroyAllWindows()

def start_server():
    uvicorn.run(app, host="0.0.0.0", port=8080)

if __name__ == "__main__":
    handler = VideoHandler()
    # Run the server in a separate thread so the camera loop doesn't stop
    threading.Thread(target=start_server, daemon=True).start()
    handler.run_camera()
