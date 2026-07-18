import logging
from typing import Callable, Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("EventHooks")

# Define event type constants
USER_REGISTERED = "USER_REGISTERED"
PROFILE_COMPLETED = "PROFILE_COMPLETED"
ASSESSMENT_STARTED = "ASSESSMENT_STARTED"
QUESTION_ANSWERED = "QUESTION_ANSWERED"
ASSESSMENT_COMPLETED = "ASSESSMENT_COMPLETED"

# Local synchronous registry for subscribers
_subscribers: Dict[str, List[Callable[..., None]]] = {
    USER_REGISTERED: [],
    PROFILE_COMPLETED: [],
    ASSESSMENT_STARTED: [],
    QUESTION_ANSWERED: [],
    ASSESSMENT_COMPLETED: []
}

def subscribe(event_type: str, callback: Callable[..., None]) -> None:
    if event_type in _subscribers:
        _subscribers[event_type].append(callback)
        logger.info(f"Subscribed {callback.__name__} to event: {event_type}")

def dispatch(event_type: str, *args, **kwargs) -> None:
    logger.info(f"Dispatching event: {event_type} with args: {args}, kwargs: {kwargs}")
    if event_type in _subscribers:
        for callback in _subscribers[event_type]:
            try:
                callback(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error executing callback {callback.__name__} for event {event_type}: {e}")

# Default fallback listener to show hooks work
def log_event_listener(event_type: str, payload: dict):
    logger.info(f"-[EVENT LOGGED]- Type: {event_type} | Payload: {payload}")

# Register default listener
for evt in _subscribers.keys():
    subscribe(evt, lambda payload, e_type=evt: log_event_listener(e_type, payload))
