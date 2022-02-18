from streamer import app
from waitress import serve
import cv2

if __name__ == "__main__":
  serve(
    app,
    host='0.0.0.0',
    port=5001,
    threads=3
  )