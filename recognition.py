import cv2
import mediapipe as mp
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import GestureRecognizerOptions
from typing import Callable, Optional

from gestures import Gesture


MPGestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

# Create a hand drawing utility from MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


class GestureRecognizer:
    """
    A class that recognizes hand gestures using MediaPipe's GestureRecognizer.

    Attributes:
        model_path (str): Path to the gesture recognition model.
        recognizer (MPGestureRecognizer): MediaPipe gesture recognizer instance.
        recognized_gesture (Optional[str]): The name of the recognized gesture.
        callback (Optional[Callable]): Optional callback function to be triggered on gesture recognition.
    """

    def __init__(self, model_path: str):
        """
        Initializes the gesture recognizer with the provided model path.

        Args:
            model_path (str): Path to the gesture recognition model.
        """
        self.model_path = model_path
        options = GestureRecognizerOptions(
            base_options=BaseOptions(model_asset_path=model_path),
            running_mode=VisionRunningMode.LIVE_STREAM,
            result_callback=self.on_gesture_recognized
        )
        self.recognizer = MPGestureRecognizer.create_from_options(options)
        self.recognized_gesture: Optional[Gesture] = None  # Store recognized gesture as Gesture Enum
        self.callback: Optional[Callable] = None

    def recognize_gesture(self, frame: cv2.Mat, timestamp: int) -> None:
        """
        Recognizes gestures in the provided frame asynchronously.

        Args:
            frame (cv2.Mat): The frame captured by the camera (BGR format).
            timestamp (int): Timestamp of the frame in milliseconds.
        """
        # Convert the frame from OpenCV to MediaPipe's Image object
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        self.recognizer.recognize_async(mp_image, timestamp)

    def on_gesture_recognized(self, result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int) -> \
            Optional[Callable]:
        """
        Callback function triggered when a gesture is recognized.

        Args:
            result (GestureRecognizerResult): The result of the gesture recognition process.
            output_image (mp.Image): The processed image from the recognizer.
            timestamp_ms (int): The timestamp of the gesture recognition event.

        Returns:
            Optional[Callable]: Calls the registered callback function, if set.
        """
        if result.gestures:
            recognized_gesture_str = result.gestures[0][0].category_name  # Get the name of the first recognized gesture
            try:
                # Convert the gesture string to the corresponding Gesture enum
                self.recognized_gesture = Gesture(recognized_gesture_str)
            except ValueError:
                # Handle the case where the recognized gesture is not in the Gesture enum
                # print(f"Unrecognized gesture: {recognized_gesture_str}")
                self.recognized_gesture = None
        else:
            self.recognized_gesture = None
            # print("No gesture recognized")

        if self.callback:
            return self.callback(result, output_image, timestamp_ms)

    def set_callback(self, callback: Callable) -> None:
        """
        Registers a callback function to be triggered on gesture recognition.

        Args:
            callback (Callable): A function to call when a gesture is recognized.
        """
        self.callback = callback

    def __del__(self):
        """Destructor to ensure the recognizer is properly closed."""
        self.recognizer.close()


def draw_landmarks(image: cv2.Mat) -> cv2.Mat:
    """
    Draws hand landmarks on the given image using MediaPipe's hand tracking.

    Args:
        image (cv2.Mat): The image where hand landmarks will be drawn (BGR format).

    Returns:
        cv2.Mat: The image with hand landmarks drawn.
    """
    with mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5) as hands:
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB for hand tracking
        results = hands.process(image_rgb)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    return image
