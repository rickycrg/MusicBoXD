import hashlib
import hmac
import secrets

import pandas as pd

from src.d1 import query, query_one

PBKDF2_ITERATIONS = 600_000

# ===================== Users =====================

def _hash_password(password, salt=None, iterations=PBKDF2_ITERATIONS):
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), iterations)
    return f"pbkdf2_sha256${iterations}${salt}${digest.hex()}"

def _check_password(password, stored):
    _, iterations, salt, _ = stored.split("$")
    return hmac.compare_digest(_hash_password(password, salt, int(iterations)), stored)

def register_user(username, email, password, name=None, surname=None, phone_num=None):
    """Create a new user and return its user_id, or None if username/email are already taken."""
    taken = query_one("SELECT 1 FROM users WHERE username = ? OR email = ?", [username, email])
    if taken:
        return None

    row = query_one(
        "INSERT INTO users (username, name, surname, email, phone_num, password_hash) "
        "VALUES (?, ?, ?, ?, ?, ?) RETURNING user_id",
        [username, name, surname, email, phone_num, _hash_password(password)],
    )
    return row["user_id"]

def login_user(username, password):
    """Return the user_id if the credentials are correct, otherwise None."""
    row = query_one("SELECT user_id, password_hash FROM users WHERE username = ?", [username])
    if row and _check_password(password, row["password_hash"]):
        return row["user_id"]
    return None

# ===================== Music =====================

def _ask_artist_type(name):
    while True:
        x = input(f"is {name} a person or a group? (p/g): ").strip().lower()
        if x in ("p", "person"):
            return "person"
        if x in ("g", "group"):
            return "group"
        print("invalid input")

def _get_or_create_artist(name):
    row = query_one("SELECT artist_id FROM artists WHERE name = ?", [name])
    if row:
        return row["artist_id"]

    row = query_one(
        "INSERT INTO artists (name, type) VALUES (?, ?) RETURNING artist_id",
        [name, _ask_artist_type(name)],
    )
    return row["artist_id"]

def _get_or_create_album(name, release_date, artist_id):
    row = query_one("SELECT album_id FROM albums WHERE name = ? AND artist_id = ?", [name, artist_id])
    if row:
        return row["album_id"]

    row = query_one(
        "INSERT INTO albums (name, release_date, artist_id) VALUES (?, ?, ?) RETURNING album_id",
        [name, release_date, artist_id],
    )
    return row["album_id"]

def _get_or_create_track(name, spotify_id, artist_ids, bpm):
    """
    Tracks are identified by their spotify id. Tracks saved before the spotify id
    existed are matched by name and main artist, and get the id filled in.
    """
    row = query_one("SELECT track_id FROM tracks WHERE spotify_id = ?", [spotify_id]) if spotify_id else None
    if not row:
        row = query_one(
            "SELECT t.track_id FROM tracks t "
            "JOIN track_artists ta ON ta.track_id = t.track_id "
            "WHERE t.name = ? AND ta.artist_id = ? AND ta.role = 'main' AND t.spotify_id IS NULL",
            [name, artist_ids[0]],
        )
    if row:
        query(
            "UPDATE tracks SET bpm = COALESCE(?, bpm), spotify_id = COALESCE(spotify_id, ?) WHERE track_id = ?",
            [bpm, spotify_id, row["track_id"]],
        )
        return row["track_id"]

    track_id = query_one(
        "INSERT INTO tracks (name, spotify_id, bpm) VALUES (?, ?, ?) RETURNING track_id",
        [name, spotify_id, bpm],
    )["track_id"]

    for i, artist_id in enumerate(artist_ids):
        query(
            "INSERT OR IGNORE INTO track_artists (track_id, artist_id, role) VALUES (?, ?, ?)",
            [track_id, artist_id, "main" if i == 0 else "featured"],
        )
    return track_id

def save_review(user_id, track, vote, opinion, bpm):
    """
    Store the track (with its artists and album) if it is new, then save the user's review.
    A second review of the same track by the same user replaces the first one.
    """
    artist_ids = [_get_or_create_artist(name) for name in track["artists"]]
    album_artist_id = _get_or_create_artist(track["album_artist"])
    album_id = _get_or_create_album(track["album"], track["release_date"], album_artist_id)
    track_id = _get_or_create_track(track["name"], track.get("spotify_id"), artist_ids, None if bpm < 0 else bpm)

    if track.get("track_number"):
        query(
            "INSERT OR IGNORE INTO album_tracks (album_id, track_id, track_num) VALUES (?, ?, ?)",
            [album_id, track_id, track["track_number"]],
        )

    query(
        "INSERT INTO track_reviews (user_id, track_id, vote, review_text) VALUES (?, ?, ?, ?) "
        "ON CONFLICT (user_id, track_id) DO UPDATE SET "
        "vote = excluded.vote, review_text = excluded.review_text, review_date = CURRENT_TIMESTAMP",
        [user_id, track_id, vote, opinion],
    )

    print(f"opinion to {track['name']} submitted!")

def get_reviews(user_id):
    """Return the user's track reviews as a DataFrame."""
    rows = query(
        "SELECT t.name AS 'song name', a.name AS artist, t.bpm, al.release_date AS 'release date', "
        "r.vote, r.review_text AS opinion "
        "FROM track_reviews r "
        "JOIN tracks t ON t.track_id = r.track_id "
        "LEFT JOIN track_artists ta ON ta.track_id = t.track_id AND ta.role = 'main' "
        "LEFT JOIN artists a ON a.artist_id = ta.artist_id "
        "LEFT JOIN album_tracks at ON at.track_id = t.track_id "
        "LEFT JOIN albums al ON al.album_id = at.album_id "
        "WHERE r.user_id = ? "
        "GROUP BY r.track_id",
        [user_id],
    )
    return pd.DataFrame(rows, columns=["song name", "artist", "bpm", "release date", "vote", "opinion"])
