-- MusicBoXD schema (SQLite / Cloudflare D1)
-- Translated from the final ER model.
--
-- Local SQLite testing: run `PRAGMA foreign_keys = ON;` first,
-- otherwise foreign keys are not enforced. D1 enforces them by default.

-- ===================== Entities =====================

CREATE TABLE users (
    user_id       INTEGER PRIMARY KEY,
    username      TEXT    NOT NULL UNIQUE,
    name          TEXT,
    surname       TEXT,
    email         TEXT    NOT NULL UNIQUE,
    phone_num     TEXT,
    password_hash TEXT    NOT NULL
);

CREATE TABLE artists (
    artist_id INTEGER PRIMARY KEY,
    name      TEXT    NOT NULL,
    type      TEXT    NOT NULL CHECK (type IN ('person', 'group')),
    region    TEXT,
    biography TEXT
);

-- releases: artist (0,N) -- album (1,1)  =>  1:N, foreign key on albums
CREATE TABLE albums (
    album_id     INTEGER PRIMARY KEY,
    name         TEXT    NOT NULL,
    release_date TEXT,                       -- ISO 8601: 'YYYY-MM-DD'
    artist_id    INTEGER NOT NULL
                 REFERENCES artists(artist_id) ON DELETE RESTRICT
);

CREATE TABLE tracks (
    track_id INTEGER PRIMARY KEY,
    name     TEXT    NOT NULL,
    bpm      REAL                            -- computed from audio, NULL if unknown
);

-- ============ N:M relationships (junction tables) ============

-- contains: album (1,N) -- track (1,N), attribute track_num
CREATE TABLE album_tracks (
    album_id  INTEGER NOT NULL REFERENCES albums(album_id) ON DELETE CASCADE,
    track_id  INTEGER NOT NULL REFERENCES tracks(track_id) ON DELETE CASCADE,
    track_num INTEGER NOT NULL CHECK (track_num > 0),
    PRIMARY KEY (album_id, track_id),
    UNIQUE (album_id, track_num)             -- no two tracks in the same slot
);

-- performs: artist (0,N) -- track (1,N), attribute role
CREATE TABLE track_artists (
    track_id  INTEGER NOT NULL REFERENCES tracks(track_id)   ON DELETE CASCADE,
    artist_id INTEGER NOT NULL REFERENCES artists(artist_id) ON DELETE CASCADE,
    role      TEXT    NOT NULL DEFAULT 'main' CHECK (role IN ('main', 'featured')),
    PRIMARY KEY (track_id, artist_id)
);

-- reviewsAlb: user (0,N) -- album (0,N)
CREATE TABLE album_reviews (
    user_id     INTEGER NOT NULL REFERENCES users(user_id)   ON DELETE CASCADE,
    album_id    INTEGER NOT NULL REFERENCES albums(album_id) ON DELETE CASCADE,
    vote        INTEGER NOT NULL CHECK (vote BETWEEN 1 AND 10),
    review_text TEXT,
    review_date TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, album_id)
);

-- reviewsTra: user (0,N) -- track (0,N)
CREATE TABLE track_reviews (
    user_id     INTEGER NOT NULL REFERENCES users(user_id)   ON DELETE CASCADE,
    track_id    INTEGER NOT NULL REFERENCES tracks(track_id) ON DELETE CASCADE,
    vote        INTEGER NOT NULL CHECK (vote BETWEEN 1 AND 10),
    review_text TEXT,
    review_date TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, track_id)
);

-- ===================== Indexes =====================
-- The composite PKs already index lookups by their first column.
-- These cover the reverse direction (e.g. "all tracks of an artist").

CREATE INDEX idx_albums_artist        ON albums(artist_id);
CREATE INDEX idx_album_tracks_track   ON album_tracks(track_id);
CREATE INDEX idx_track_artists_artist ON track_artists(artist_id);
CREATE INDEX idx_album_reviews_album  ON album_reviews(album_id);
CREATE INDEX idx_track_reviews_track  ON track_reviews(track_id);