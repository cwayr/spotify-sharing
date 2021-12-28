from flask import session

def clear_session():
        """Clears session of selected Spotify song data."""

        session.pop("track_image", None)
        session.pop("track_name", None)
        session.pop("track_artist", None)
        session.pop("track_link", None)
        session.pop("track_preview", None)