from dataclasses import dataclass
@dataclass
class Album:
    AlbumId: int
    Title: str
    ArtistId: int
    millisecondi: int

    def __str__(self):
        return f"{self.Title} - {self.ArtistId} - {self.AlbumId}"

    def __hash__(self):
        return hash(self.AlbumId)