from database.DB_connect import DBConnect
from model.album import Album



class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAlbum(secondi):
        conn = DBConnect.get_connection()

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT a.AlbumId , a.Title , a.ArtistId, s.millisecondi
                    FROM album a, (SELECT DISTINCT t.AlbumId, SUM(t.Milliseconds) as millisecondi
                    FROM track t 
                    GROUP BY t.AlbumId ) as s
                    WHERE a.AlbumId = s.AlbumId and s.millisecondi>%s"""

        cursor.execute(query, (secondi,))

        result = []
        for row in cursor:
            result.append(Album(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getedges(secondi):
        conn = DBConnect.get_connection()

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT t1.AlbumId as v0, t2.AlbumId as v1 
                    FROM 
                    (SELECT t.TrackId, t.Name, t.AlbumId, p.PlaylistId 
                    FROM track t, playlisttrack p 
                    Where t.TrackId = p.TrackId and t.AlbumId IN (SELECT DISTINCT a.AlbumId
                                        FROM album a, (SELECT DISTINCT t.AlbumId, SUM(t.Milliseconds) as millisecondi
                                        FROM track t 
                                        GROUP BY t.AlbumId ) as s
                                        WHERE a.AlbumId = s.AlbumId and s.millisecondi>%s)) as t1, (SELECT t.TrackId, t.Name, t.AlbumId, p.PlaylistId 
                    FROM track t, playlisttrack p 
                    Where t.TrackId = p.TrackId and t.AlbumId IN (SELECT DISTINCT a.AlbumId
                                        FROM album a, (SELECT DISTINCT t.AlbumId, SUM(t.Milliseconds) as millisecondi
                                        FROM track t 
                                        GROUP BY t.AlbumId ) as s
                                        WHERE a.AlbumId = s.AlbumId and s.millisecondi>%s)) as t2
                    Where t1.AlbumId!=t2.AlbumId and t1.PlaylistId=t2.PlaylistId"""

        cursor.execute(query, (secondi,secondi,))

        result = []
        for row in cursor:
            result.append((row["v0"], row["v1"]))

        cursor.close()
        conn.close()
        return result
