# Gestify 🎵✋

**Gestify** is a gesture-based control system for Spotify, allowing users to manage their music playback using simple hand gestures. Through gesture recognition via a webcam, users can pause, play, skip tracks, adjust volume, and even like songs with intuitive gestures—no need to touch a device!

## Features

- **Gesture Recognition**: Supports several hand gestures to perform various actions.
- **Spotify Control**: Uses the Spotify Web API to control playback, volume, and playlist actions.
- **Easy Setup**: Leverages MediaPipe for gesture recognition and Spotipy for Spotify integration.
- **Modular Design**: Clean and organized code with object-oriented patterns, making it easy to extend.

## Supported Gestures

- **Thumb Up**: Add the current track to your Liked Songs.
- **Thumb Down**: Skip to the next track.
- **Open Palm**: Stop playback.
- **Pointing Up**: Increase volume by 10%.
- **Victory**: Mute.
- **I Love You**: Unmute.
- **Closed Fist**: Approve action (used in combination with other gestures).

## Getting Started

### Prerequisites

- Python 3.8+
- Spotify Premium account (for full API access)
- Webcam (for gesture recognition)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/gestify.git
    cd gestify
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt```

3. Set up your Spotify API credentials:

    Create a `.env` file in the root directory with the following content:

    ```bash
    SPOTIPY_CLIENT_ID=your-client-id
    SPOTIPY_CLIENT_SECRET=your-client-secret
    SPOTIPY_REDIRECT_URI=http://localhost:3000
    ```

    You can get your Spotify credentials by registering your app at the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).

### Usage

Run the application:

```bash
python gesture-app.py
```

## Usage

Once running, Gestify will detect your hand gestures through your webcam and control Spotify accordingly.

## Gesture Mapping

The default gestures are mapped to the following actions:

| Gesture       | Action                         |
|---------------|--------------------------------|
| Thumb Up      | Add current track to Liked     |
| Thumb Down    | Play next track                |
| Open Palm     | Stop playback                  |
| Pointing Up   | Increase volume by 10%         |
| Victory       | Mute                           |
| I Love You    | Unmute                         |
| Closed Fist   | Approve Action                 |

## Customizing Gestures

You can modify the gesture-action mappings by editing the `add_gesture_mappings()` method in `action_manager.py`.

## Contributing

If you'd like to contribute to Gestify, feel free to submit issues or pull requests. Any suggestions for improving the project are welcome!

## License

This project is licensed under the MIT License.
