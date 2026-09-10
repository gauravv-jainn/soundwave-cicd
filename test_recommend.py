from recommend import score_song, recommend_songs


CATALOG = [
    {"id": "s1", "title": "Neon Nights", "artist": "Aria Vale", "popularity": 40},
    {"id": "s2", "title": "Slow Tide", "artist": "Aria Vale", "popularity": 55},
    {"id": "s3", "title": "Concrete Sky", "artist": "The Driftwood", "popularity": 90},
    {"id": "s4", "title": "Paper Planes Redux", "artist": "Mono Static", "popularity": 20},
]


def test_score_song_favours_liked_artist():
    liked = [{"id": "s1", "artist": "Aria Vale"}]
    score = score_song(CATALOG[1], liked, play_counts={})
    assert score == 5  # same artist as a liked song


def test_score_song_adds_play_count():
    liked = []
    score = score_song(CATALOG[2], liked, play_counts={"s3": 3})
    assert score == 3


def test_score_song_bonus_for_already_liked():
    liked = [{"id": "s1", "artist": "Aria Vale"}]
    score = score_song(CATALOG[0], liked, play_counts={"s1": 2})
    assert score == 5 + 2 + 2  # artist match + play count + liked bonus


def test_recommend_songs_returns_top_n():
    liked = [{"id": "s2", "artist": "Aria Vale"}]
    play_counts = {"s2": 4, "s3": 1}
    result = recommend_songs(CATALOG, liked, play_counts, top_n=2)
    assert len(result) == 2
    assert result[0]["id"] == "s2"  # liked + played the most + artist match


def test_recommend_songs_falls_back_to_trending_for_new_user():
    result = recommend_songs(CATALOG, liked_songs=[], play_counts={}, top_n=1)
    assert result[0]["id"] == "s3"  # highest popularity
