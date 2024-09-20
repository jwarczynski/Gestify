from gestures import GestureAction, GestureToActionMapper, Gesture


class GestureState:
    """Base class for handling gestures in different states."""

    def handle_gesture(self, gesture: Gesture, context: 'ActionApprovalManager') -> None:
        raise NotImplementedError("Subclasses must implement this method.")


class IdleState(GestureState):
    """Default state, waiting for a gesture."""

    def handle_gesture(self, gesture: Gesture, context: 'ActionApprovalManager') -> None:
        if gesture == Gesture.CLOSED_FIST:
            return None  # this gesture is only for approval
        if gesture in context.mapper.gesture_action_map:
            context.transition_to(ActionDetectedState())
            context.pending_gesture = gesture
            print(f"Gesture '{gesture.value}' detected. Waiting for approval...")


class ActionDetectedState(GestureState):
    """State after a gesture is detected, waiting for approval."""

    def handle_gesture(self, gesture: Gesture, context: 'ActionApprovalManager') -> None:
        if gesture == Gesture.CLOSED_FIST:
            context.transition_to(ApprovedState())
            context.execute_action()


class ApprovedState(GestureState):
    """State when the gesture is approved, action is performed, returns to Idle."""

    def handle_gesture(self, gesture: Gesture, context: 'ActionApprovalManager') -> None:
        context.transition_to(IdleState())


class ActionApprovalManager:
    """Manages the states and transitions between them."""

    def __init__(self, mapper: GestureToActionMapper) -> None:
        self.state: GestureState = IdleState()
        self.pending_gesture: Gesture | None = None
        self.mapper = mapper

    def transition_to(self, state: GestureState) -> None:
        self.state = state

    def handle_gesture(self, gesture: Gesture) -> None:
        self.state.handle_gesture(gesture, self)

    def execute_action(self) -> None:
        if self.pending_gesture:
            action: GestureAction = self.mapper.gesture_action_map.get(self.pending_gesture)
            if action:
                print(f"Performing action: {action.action_name}")
                action.perform_action()
            self.pending_gesture = None

    def __repr__(self) -> str:
        return f"ApprovalManager(state={self.state.__class__.__name__}, gesture={self.pending_gesture})"
