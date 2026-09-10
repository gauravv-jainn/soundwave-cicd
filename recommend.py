"""SoundWave recommendation utility.

Given a listener's liked songs and play history, this module scores and
ranks songs from the catalog to build the "Recommended for You" list
described in the SRS (section 4.6 Music Recommendations, FR-20, FR-21).
"""


def score_song(song, liked_songs, play_counts):
    """Return a relevance score for a single song.

    +5 if the song's artist matches an artist the user has liked.
    +1 for every previous play of this exact song.
    +2 bonus if the song itself is already liked.
    """
    score = 0
    liked_artists = {liked["artist"] for liked in liked_songs}
    if song["artist"] in liked_artists:
        score += 5
    score += play_counts.get(song["id"], 0)
    if song["id"] in {liked["id"] for liked in liked_songs}:
        score += 2
    return score


def recommend_songs(catalog, liked_songs, play_counts, top_n=5):
    """Rank the catalog and return the top_n recommended songs.

    Falls back to trending/popular songs when the user has no listening
    history yet (FR-21).
    """
    if not liked_songs and not play_counts:
        trending = sorted(catalog, key=lambda s: s.get("popularity", 0), reverse=True)
        return trending[:top_n]

    ranked = sorted(
        catalog,
        key=lambda s: score_song(s, liked_songs, play_counts),
        reverse=True,
    )
    return ranked[:top_n]


if __name__ == "__main__":
    catalog = [
        {"id": "s1", "title": "Neon Nights", "artist": "Aria Vale", "popularity": 40},
        {"id": "s2", "title": "Slow Tide", "artist": "Aria Vale", "popularity": 55},
        {"id": "s3", "title": "Concrete Sky", "artist": "The Driftwood", "popularity": 90},
        {"id": "s4", "title": "Paper Planes Redux", "artist": "Mono Static", "popularity": 20},
    ]
    liked_songs = [{"id": "s2", "artist": "Aria Vale"}]
    play_counts = {"s2": 4, "s3": 1}

    print("SOUNDWAVE RECOMMENDATION DEMO")
    print("Liked songs:", [s["id"] for s in liked_songs])
    print("Play counts:", play_counts)

    top_picks = recommend_songs(catalog, liked_songs, play_counts, top_n=3)
    print("Recommended for You:")
    for song in top_picks:
        print(" -", song["title"], "by", song["artist"])
