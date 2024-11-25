from flask import Flask, request, jsonify
from Classes import Song, LinkedList, Playlist
app = Flask(__name__)


songs = {}
playlists = {}


# Song Endpoints

@app.route('/songs', methods=['POST'])
def create_song():
    data = request.json
    song_id = int(data['id'])  # Ensure the ID is an integer
    if song_id in songs:
        return jsonify({'message': 'Song already exists.'}), 400
    songs[song_id] = Song(song_id, data['name'], data['artist'], data['genre'])
    return jsonify({'message': 'Song created.'}), 201

@app.route('/songs/<int:song_id>', methods=['GET'])
def get_song(song_id):
    if song_id not in songs:
        return jsonify({'message': 'Song not found.'}), 404
    song = songs[song_id]
    return jsonify({'id': song.id, 'name': song.name, 'artist': song.artist, 'genre': song.genre}), 200

@app.route('/songs/<int:song_id>', methods=['PUT'])
def update_song(song_id):
    if song_id not in songs:
        return jsonify({'message': 'Song not found.'}), 404
    data = request.json
    song = songs[song_id]
    song.name = data.get('name', song.name)
    song.artist = data.get('artist', song.artist)
    song.genre = data.get('genre', song.genre)
    return jsonify({'message': 'Song updated.'}), 200

@app.route('/songs/<int:song_id>', methods=['DELETE'])
def delete_song(song_id):
    if song_id not in songs:
        return jsonify({'message': 'Song not found.'}), 404
    del songs[song_id]
    return jsonify({'message': 'Song deleted.'}), 200

@app.route('/songs/search', methods=['GET'])
def search_songs():
    query = request.args.get('query')
    attribute = request.args.get('attribute', 'name')
    results = [song.__dict__ for song in songs.values() if query.lower() in getattr(song, attribute).lower()]
    return jsonify(results), 200

# Playlist Endpoints

@app.route('/playlists', methods=['POST'])
def create_playlist():
    data = request.json
    playlist_id = int(data['id'])  # Ensure the ID is an integer
    if playlist_id in playlists:
        return jsonify({'message': 'Playlist already exists.'}), 400
    playlists[playlist_id] = Playlist(playlist_id, data['name'])
    return jsonify({'message': 'Playlist created.'}), 201

@app.route('/playlists/<int:playlist_id>', methods=['GET'])
def get_playlist(playlist_id):
    if playlist_id not in playlists:
        return jsonify({'message': 'Playlist not found.'}), 404
    playlist = playlists[playlist_id]
    return jsonify({'id': playlist.id, 'name': playlist.name, 'songs': playlist.get_songs()}), 200

@app.route('/playlists/<int:playlist_id>', methods=['PUT'])
def update_playlist(playlist_id):
    if playlist_id not in playlists:
        return jsonify({'message': 'Playlist not found.'}), 404
    data = request.json
    playlist = playlists[playlist_id]
    playlist.name = data.get('name', playlist.name)
    return jsonify({'message': 'Playlist updated.'}), 200

@app.route('/playlists/<int:playlist_id>', methods=['DELETE'])
def delete_playlist(playlist_id):
    if playlist_id not in playlists:
        return jsonify({'message': 'Playlist not found.'}), 404
    del playlists[playlist_id]
    return jsonify({'message': 'Playlist deleted.'}), 200

# Additional Endpoints

@app.route('/playlists/<int:playlist_id>/songs', methods=['POST'])
def add_song_to_playlist(playlist_id):
    if playlist_id not in playlists:
        return jsonify({'message': 'Playlist not found.'}), 404
    data = request.json
    song_id = int(data['song_id'])  # Ensure the ID is an integer
    if song_id not in songs:
        return jsonify({'message': 'Song not found.'}), 404
    playlists[playlist_id].add_song(song_id)
    return jsonify({'message': 'Song added to playlist.'}), 200

@app.route('/playlists/<int:playlist_id>/songs/<int:song_id>', methods=['DELETE'])
def remove_song_from_playlist(playlist_id, song_id):
    if playlist_id not in playlists:
        return jsonify({'message': 'Playlist not found.'}), 404
    playlists[playlist_id].remove_song(song_id)
    return jsonify({'message': f'Song with ID {song_id} removed from playlist.'}), 200

@app.route('/playlists/<int:playlist_id>/sort', methods=['GET'])
def sort_songs_in_playlist(playlist_id):
    if playlist_id not in playlists:
        return jsonify({'message': 'Playlist not found.'}), 404
    sort_by = request.args.get('sort_by', 'name')
    playlist = playlists[playlist_id]
    sorted_songs = sorted(playlist.get_songs(), key=lambda song_id: getattr(songs[song_id], sort_by))
    playlist.songs = LinkedList()
    for song_id in sorted_songs:
        playlist.add_song(song_id)
    return jsonify({'message': f'Songs sorted by {sort_by}.'}), 200

# Running the Flask app
if __name__ == '__main__':
    app.run(debug=True)
