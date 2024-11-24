from flask import Flask, request, jsonify

app = Flask(__name__)

songs = {}
playlists = {}

class Song:
    def __init__(self, song_id, name, artist, genre):
        self.id = song_id
        self.name = name
        self.artist = artist
        self.genre = genre

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def prepend(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def delete_with_value(self, data):
        if not self.head:
            return
        if self.head.data == data:
            self.head = self.head.next
            return
        current = self.head
        while current.next and current.next.data != data:
            current = current.next
        if current.next:
            current.next = current.next.next

    def to_list(self):
        elements = []
        current = self.head
        while current:
            elements.append(current.data)
            current = current.next
        return elements

class Playlist:
    def __init__(self, playlist_id, name):
        self.id = playlist_id
        self.name = name
        self.songs = LinkedList()

    def add_song(self, song_id):
        self.songs.append(song_id)

    def remove_song(self, song_id):
        self.songs.delete_with_value(song_id)

    def get_songs(self):
        return self.songs.to_list()

# Song Endpoints

@app.route('/songs', methods=['POST'])
def create_song():
    data = request.json
    song_id = data['id']
    if song_id in songs:
        return jsonify({'message': 'Song already exists.'}), 400
    songs[song_id] = Song(song_id, data['name'], data['artist'], data['genre'])
    return jsonify({'message': 'Song created.'}), 201

@app.route('/songs/<song_id>', methods=['PUT'])
def update_song(song_id):
    if song_id not in songs:
        return jsonify({'message': 'Song not found.'}), 404
    data = request.json
    song = songs[song_id]
    song.name = data.get('name', song.name)
    song.artist = data.get('artist', song.artist)
    song.genre = data.get('genre', song.genre)
    return jsonify({'message': 'Song updated.'}), 200

@app.route('/songs/<song_id>', methods=['DELETE'])
def delete_song(song_id):
    if song_id not in songs:
        return jsonify({'message': 'Song not found.'}), 404
    del songs[song_id]
    return jsonify({'message': 'Song deleted.'}), 200

@app.route('/songs/<song_id>', methods=['GET'])
def get_song(song_id):
    if song_id not in songs:
        return jsonify({'message': 'Song not found.'}), 404
    song = songs[song_id]
    return jsonify({'id': song.id, 'name': song.name, 'artist': song.artist, 'genre': song.genre}), 200

@app.route('/songs/search', methods=['GET'])
def search_songs():
    query = request.args.get('query')
    attribute = request.args.get('attribute', 'name')
    results = [song.__dict__ for song in songs.values() if query.lower() in getattr(song, attribute).lower()]
    return jsonify(results), 200

