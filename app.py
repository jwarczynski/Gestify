import time

import cv2

from camera import CameraCapture
from states import ActionApprovalManager
from spotify import SpotifyController
from recognition import GestureRecognizer, draw_landmarks
from gestures import GestureToActionMapper, GestureAction, Gesture


class ApplicationController:
    """
    The main controller that manages the camera feed, gesture recognition, and Spotify control.

    Attributes:
        camera (CameraCapture): Manages the camera capture.
        recognizer (GestureRecognizer): Recognizes hand gestures.
        spotify_controller (SpotifyController): Controls Spotify actions.
        mapper (GestureToActionMapper): Maps gestures to corresponding actions.
        approval_manager (ActionApprovalManager): Manages gesture approvals.
    """

    def __init__(self) -> None:
        """Initializes the ApplicationController and sets up gesture mappings."""
        self.camera = CameraCapture()
        self.recognizer = GestureRecognizer("gesture_recognizer.task")
        self.spotify_controller = SpotifyController.get_instance()
        self.mapper = GestureToActionMapper()
        self.approval_manager = ActionApprovalManager(self.mapper)
        self.add_gesture_mappings()

    def run(self) -> None:
        """Starts the camera feed and begins processing each frame."""
        self.camera.start_capture(self.process_frame)

    def process_frame(self, frame: cv2.Mat) -> None:
        """
        Processes each frame from the camera, recognizes gestures, and maps them to actions.

        Args:
            frame (cv2.Mat): The current frame from the camera feed.
        """
        timestamp = int((time.time() - self.camera.start_time) * 1000)  # Use current timestamp
        self.recognizer.recognize_gesture(frame, timestamp)

        # Display recognized gesture on the frame
        cv2.putText(frame, f'Gesture: {self.recognizer.recognized_gesture}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 0), 2)
        draw_landmarks(frame)
        cv2.imshow('Gesture Recognition', frame)

        # Handle gesture approval before performing any action
        self.approval_manager.handle_gesture(self.recognizer.recognized_gesture)

    def on_gesture_recognized(self, gesture: Gesture) -> None:
        """
        Called when a gesture is recognized to map it to the corresponding action.

        Args:
            gesture (Gesture): The name of the recognized gesture.
        """
        self.mapper.map_gesture_to_action(gesture)

    def add_gesture_mappings(self) -> None:
        """Defines the gesture-to-action mappings for Spotify controls."""
        # Mapping gestures to Spotify actions
        self.mapper.add_mapping(Gesture.THUMB_UP,
                                GestureAction("Add to Liked", self.spotify_controller.add_current_track_to_liked))
        self.mapper.add_mapping(Gesture.THUMB_DOWN,
                                GestureAction("Play Next", self.spotify_controller.play_next_track))
        self.mapper.add_mapping(Gesture.OPEN_PALM,
                                GestureAction("Stop Playback", self.spotify_controller.stop_playback))
        self.mapper.add_mapping(Gesture.POINTING_UP,
                                GestureAction("Increase Volume", self.spotify_controller.increment_volume))
        self.mapper.add_mapping(Gesture.VICTORY,
                                GestureAction("Mute", self.spotify_controller.mute))
        self.mapper.add_mapping(Gesture.I_LOVE_YOU,
                                GestureAction("Unmute", self.spotify_controller.unmute))

        def not_implemented_action() -> None:
            """Placeholder action for unimplemented gestures."""
            raise NotImplementedError("Action not implemented")

        self.mapper.add_mapping(Gesture.CLOSED_FIST,
                                GestureAction("Approve", not_implemented_action))


if __name__ == "__main__":
    app = ApplicationController()
    app.run()
    cv2.destroyAllWindows()
