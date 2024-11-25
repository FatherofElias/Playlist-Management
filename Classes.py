from Node import Node

class Song:
    def __init__(self, song_id, name, artist, genre):
        self.id = song_id
        self.name = name
        self.artist = artist
        self.genre = genre



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