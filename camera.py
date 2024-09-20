import time

import cv2
from typing import Callable


class CameraCapture:
    """
    A class to manage video capture from a camera source and pass each frame to a callback for processing.

    Attributes:
        cap (cv2.VideoCapture): The OpenCV video capture object.
        start_time (float): The timestamp when the capture started.
    """

    def __init__(self, source: int = 0) -> None:
        """
        Initializes the CameraCapture object with the specified video source.

        Args:
            source (int): The index of the camera (default is 0, usually the first webcam).
        """
        self.cap: cv2.VideoCapture = cv2.VideoCapture(source)
        self.start_time: float = time.time()

    def start_capture(self, frame_callback: Callable[[cv2.Mat], None]) -> None:
        """
        Starts capturing video frames from the camera and processes them using a callback function.

        Args:
            frame_callback (Callable[[cv2.Mat], None]): A function that processes each video frame.
        """
        while self.cap.isOpened():
            success, frame = self.cap.read()
            if success:
                frame_callback(frame)
            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.cap.release()
