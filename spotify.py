import os

import spotipy
from spotipy import SpotifyOAuth
from dotenv import load_dotenv
from typing import Optional
from functools import wraps
import spotipy.exceptions


def handle_spotify_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except spotipy.exceptions.SpotifyException as e:
            print(f"Spotify error in {func.__name__}: {e}")
        except Exception as e:
            print(f"Unexpected error in {func.__name__}: {e}")
    return wrapper


def ensure_device(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.device_id is None:
            self.device_id = self.get_current_device()
        return func(self, *args, **kwargs)
    return wrapper


class SpotifyController:
    """
    A singleton class to interact with the Spotify Web API, allowing control over playback and managing user actions.

    Attributes:
        sp (spotipy.Spotify): The Spotify API client instance.
        device_id (Optional[str]): The ID of the currently active Spotify device.
    """
    _instance: Optional['SpotifyController'] = None

    @staticmethod
    def get_instance() -> 'SpotifyController':
        """
        Returns the singleton instance of SpotifyController.

        Returns:
            SpotifyController: The singleton instance of the SpotifyController class.
        """
        if SpotifyController._instance is None:
            SpotifyController._instance = SpotifyController()
        return SpotifyController._instance

    def __init__(self) -> None:
        """
        Initializes the SpotifyController instance with Spotify API credentials.
        """
        load_dotenv()
        if SpotifyController._instance is not None:
            raise Exception("SpotifyController is a singleton!")
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=os.getenv("SPOTIPY_CLIENT_ID"),
                client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
                redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
                scope="user-library-modify user-read-playback-state"
            )
        )
        self.device_id: Optional[str] = None

    @handle_spotify_errors
    def add_current_track_to_liked(self) -> None:
        """
        Adds the currently playing track to the user's liked songs.
        """
        current_track = self.sp.currently_playing()
        print(f'Current track: {current_track}')
        if current_track and current_track['is_playing']:
            track_id = current_track['item']['id']
            self.sp.current_user_saved_tracks_add([track_id])

    @handle_spotify_errors
    @ensure_device
    def stop_playback(self) -> None:
        """
        Stops the playback on the currently active device.
        """
        self.sp.pause_playback(device_id=self.device_id)

    @handle_spotify_errors
    @ensure_device
    def play_next_track(self) -> None:
        """
        Skips to the next track in the user's playback queue.
        """
        self.sp.next_track()

    @handle_spotify_errors
    @ensure_device
    def decrease_volume(self) -> None:
        """
        Decreases the volume of the currently active device by 10%.
        """
        current_volume = self.sp.current_playback()['device']['volume_percent']
        new_volume = max(0, current_volume - 10)
        self.sp.volume(new_volume)

    @handle_spotify_errors
    def increment_volume(self) -> None:
        """
        Increases the volume of the currently active device by 10%.
        """
        current_volume = self.sp.current_playback()['device']['volume_percent']
        new_volume = min(100, current_volume + 10)
        self.sp.volume(new_volume)

    @handle_spotify_errors
    def mute(self) -> None:
        """
        Mutes the playback by setting the volume to 0%.
        """
        self.sp.volume(0)

    @handle_spotify_errors
    def unmute(self) -> None:
        """
        Unmutes the playback by setting the volume to 100%.
        """
        self.sp.volume(100)

    @handle_spotify_errors
    def get_current_device(self) -> Optional[str]:
        """
        Retrieves the ID of the currently active device.

        Returns:
            Optional[str]: The device ID of the currently active Spotify device, or None if no active device is found.
        """
        devices = self.sp.devices()
        device = next((d for d in devices['devices'] if d['is_active']), None)
        print(f'Active device: {device}')
        return device['id'] if device else None
