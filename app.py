from flask import Flask, request, jsonify
from Classes import Song, LinkedList, Playlist
app = Flask(__name__)


songs = {}
playlists = {}


# Search and Sort Algo Time Complexity and performance trade offs

# *Search Algorithms*

# Linear Search

# Description: Iterates through each song in the playlist to find matches based on the search criteria.
# Time Complexity: 𝑂(𝑛), where 𝑛 is the number of songs.
# Space Complexity: 𝑂(1).


# Performance Trade-offs:
# Pros: Simple to implement and understand. It does not require the playlist to be sorted.
# Cons: Inefficient for large playlists as it checks each element one by one. The search time increases linearly with the size of the playlist.


# Binary Search

# Description: Searches for a song by repeatedly dividing the search interval in half. 
# The playlist must be sorted based on the search attribute.
# Time Complexity: 𝑂(log⁡𝑛).
# Space Complexity: 𝑂(1).

# Performance Trade-offs:
# Pros: Much faster than linear search for large playlists due to its logarithmic time complexity.
# Cons: Requires the playlist to be sorted, which adds overhead if the playlist changes frequently. Additionally, the search is only efficient if the dataset remains sorted or is sorted prior to the search.

# *Sort Algorithms*

# QuickSort

# Description: A divide-and-conquer algorithm that selects a 'pivot' element and partitions the array around the pivot.
# Time Complexity:
# Average Case: 𝑂(𝑛log⁡𝑛)
# Worst Case: 𝑂(𝑛^2), typically when the pivot selection is poor (e.g., the smallest or largest element is always chosen as the pivot).
# Space Complexity: 𝑂(log⁡𝑛) due to the recursion stack.

# Performance Trade-offs:
# Pros: Generally fast with a good average-case performance, and it is an in-place sort (no additional memory is required beyond the original array).
# Cons: The worst-case performance can be significantly degraded if not properly implemented with a good pivot selection strategy.

# MergeSort

# Description: Another divide-and-conquer algorithm that divides the array into halves, sorts them, and then merges the sorted halves.
# Time Complexity: 𝑂(𝑛log⁡𝑛) in all cases (best, average, and worst).
# Space Complexity: 𝑂(𝑛) due to the additional space required for merging.

# Performance Trade-offs:
# Pros: Guarantees 𝑂(𝑛log⁡𝑛) time complexity and is stable (maintains the relative order of equal elements).
# Cons: Requires additional space proportional to the size of the input array, which can be an issue for very large datasets.


# ~Application in Playlist Management~

# Searching
# Linear Search is adequate for moderate-sized playlists and scenarios where the playlist does not require sorting or the data changes frequently.
# Binary Search is preferable for larger playlists where the data remains relatively static or can be efficiently sorted prior to searches. 
# This method significantly reduces search times once the initial sorting overhead is managed.

# Sorting
# QuickSort: Suitable for most playlist sorting needs due to its efficient average-case performance. 
# It works well for in-place sorting where memory usage is a consideration.
# MergeSort: Best for scenarios where stable sorting is required, and additional memory usage is not a critical concern. 
# It offers consistent performance regardless of the input data distribution.




# Song Endpoints

@app.route('/songs', methods=['POST'])
def create_song():
    data = request.json
    try:
        song_id = int(data['id'])
    except ValueError:
        return jsonify({'message': 'Invalid ID format. ID must be an integer.'}), 400
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
    try:
        playlist_id = int(data['id'])
    except ValueError:
        return jsonify({'message': 'Invalid ID format. ID must be an integer.'}), 400
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
    try:
        song_id = int(data['song_id'])
    except ValueError:
        return jsonify({'message': 'Invalid ID format. Song ID must be an integer.'}), 400
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
    sorted_playlist = [{'id': song_id, 'name': songs[song_id].name, 'artist': songs[song_id].artist, 'genre': songs[song_id].genre} for song_id in sorted_songs]
    return jsonify({'message': f'Songs sorted by {sort_by}.', 'sorted_playlist': sorted_playlist}), 200

# Running the Flask app
if __name__ == '__main__':
    app.run(debug=True)
