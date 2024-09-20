from typing import Callable
from enum import Enum


class Gesture(Enum):
    CLOSED_FIST = "Closed_Fist"
    THUMB_UP = "Thumb_Up"
    THUMB_DOWN = "Thumb_Down"
    OPEN_PALM = "Open_Palm"
    POINTING_UP = "Pointing_Up"
    VICTORY = "Victory"
    I_LOVE_YOU = "ILoveYou"


class GestureAction:
    """
    A class representing an action to be performed based on a recognized gesture.

    Attributes:
        action_name (str): The name of the action.
        action (Callable): The function to execute for the action.
    """
    def __init__(self, action_name: str, action: Callable[[], None]) -> None:
        """
        Initializes the GestureAction object with the name of the action and the function to perform the action.

        Args:
            action_name (str): The name of the action.
            action (Callable): The function to be executed when the action is performed.
        """
        self.action_name = action_name
        self.action = action

    def perform_action(self) -> None:
        """Executes the action associated with the gesture."""
        self.action()


class GestureToActionMapper:
    """
    A class responsible for mapping gestures to corresponding actions and invoking those actions.

    Attributes:
        gesture_action_map (Dict[str, GestureAction]): A dictionary mapping gestures to their corresponding actions.
    """

    def __init__(self) -> None:
        """Initializes an empty mapping of gestures to actions."""
        self.gesture_action_map: dict[Gesture, GestureAction] = {}

    def map_gesture_to_action(self, gesture: Gesture) -> None:
        """
        Maps the recognized gesture to the corresponding action and performs the action if a mapping exists.

        Args:
            gesture (str): The name of the recognized gesture.
        """
        action = self.gesture_action_map.get(gesture)
        if action:
            action.perform_action()

    def add_mapping(self, gesture: Gesture, action: GestureAction) -> None:
        """
        Adds a mapping between a gesture and an action.

        Args:
            gesture (str): The name of the gesture.
            action (GestureAction): The action associated with the gesture.
        """
        self.gesture_action_map[gesture] = action
