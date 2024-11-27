import mysql.connector

def connect_to_db():
    """Connect to the MySQL database."""
    return mysql.connector.connect(
        host="localhost",
        user="root",  
        password="12345678",  
        database="phase" 
    )

def get_all_followers_of_artist(cursor, identifier):
    """Retrieve all users who follow a given artist by ID or name."""
    if isinstance(identifier, int):  # Search by Artist_ID
        query = """
        SELECT U.Username
        FROM User U
        JOIN UserFollowsArtist UFA ON U.User_ID = UFA.User_ID
        WHERE UFA.Artist_ID = %s;
        """
        cursor.execute(query, (identifier,))
    else:  # Search by Artist Name
        query = """
        SELECT U.Username
        FROM User U
        JOIN UserFollowsArtist UFA ON U.User_ID = UFA.User_ID
        JOIN Artists A ON UFA.Artist_ID = A.Artist_ID
        WHERE A.Name = %s;
        """
        cursor.execute(query, (identifier,))
    return cursor.fetchall()

def get_artists_in_range(cursor, min_followers, max_followers):
    """Retrieve artist names and genres with followers in a given range."""
    query = """
    SELECT A.Name, AG.GenreName
    FROM Artists A
    JOIN ArtistGenre AG ON A.Artist_ID = AG.Artist_ID
    WHERE (SELECT COUNT(*) 
           FROM UserFollowsArtist UFA
           WHERE UFA.Artist_ID = A.Artist_ID) BETWEEN %s AND %s;
    """
    cursor.execute(query, (min_followers, max_followers))
    return cursor.fetchall()

def get_average_followers(cursor):
    """Calculate the average number of followers per artist."""
    query = """
    SELECT AVG(FollowerCount) AS AverageFollowers
    FROM (
        SELECT COUNT(UFA.User_ID) AS FollowerCount
        FROM UserFollowsArtist UFA
        GROUP BY UFA.Artist_ID
    ) AS FollowerCounts;
    """
    cursor.execute(query)
    return cursor.fetchone()[0]

def search_tracks(cursor, partial_name):
    """Search for tracks that partially match a given name."""
    query = """
    SELECT Track_Name
    FROM Track
    WHERE Track_Name LIKE %s;
    """
    cursor.execute(query, (f"%{partial_name}%",))
    return cursor.fetchall()

def get_average_tracks_per_playlist(cursor):
    """Calculate the average number of tracks per playlist created by users."""
    query = """
    SELECT AVG(TrackCount) AS AverageTracks
    FROM (
        SELECT COUNT(TIP.Track_ID) AS TrackCount
        FROM TrackInPlaylist TIP
        JOIN Playlist P ON TIP.Playlist_ID = P.Playlist_ID
        GROUP BY P.Playlist_ID
    ) AS TrackCounts;
    """
    cursor.execute(query)
    return cursor.fetchone()[0]

def get_total_likes_for_artist(cursor, identifier):
    """Calculate the total likes for an artist's tracks by ID or name."""
    if isinstance(identifier, int):  # Search by Artist_ID
        query = """
        SELECT SUM(T.Likes) AS TotalLikes
        FROM Track T
        JOIN ArtistsOnTrack AOT ON T.Track_ID = AOT.Track_ID
        WHERE AOT.Artist_ID = %s;
        """
        cursor.execute(query, (identifier,))
    else:  # Search by Artist Name
        query = """
        SELECT SUM(T.Likes) AS TotalLikes
        FROM Track T
        JOIN ArtistsOnTrack AOT ON T.Track_ID = AOT.Track_ID
        JOIN Artists A ON AOT.Artist_ID = A.Artist_ID
        WHERE A.Name = %s;
        """
        cursor.execute(query, (identifier,))
    return cursor.fetchone()[0]
def get_sorted_by_genre(cursor):
    """Retrieve and sort albums, artists, and tracks by genre."""
    query_artists = """
    SELECT AG.GenreName, A.Name AS Artist_Name
    FROM Artists A
    JOIN ArtistGenre AG ON A.Artist_ID = AG.Artist_ID
    ORDER BY AG.GenreName, A.Name;
    """
    cursor.execute(query_artists)
    artists = cursor.fetchall()

    query_albums = """
    SELECT AG.GenreName, AL.Name AS Album_Name
    FROM Albums AL
    JOIN Artists AR ON AL.Artist_ID = AR.Artist_ID
    JOIN ArtistGenre AG ON AR.Artist_ID = AG.Artist_ID
    ORDER BY AG.GenreName, AL.Name;
    """
    cursor.execute(query_albums)
    albums = cursor.fetchall()

    query_tracks = """
    SELECT TG.GenreName, T.Track_Name
    FROM Track T
    JOIN TrackGenre TG ON T.Track_ID = TG.Track_ID
    ORDER BY TG.GenreName, T.Track_Name;
    """
    cursor.execute(query_tracks)
    tracks = cursor.fetchall()

    return {"artists": artists, "albums": albums, "tracks": tracks}

def main():
    db_connection = connect_to_db()
    cursor = db_connection.cursor()

    while True:
        print("\nChoose an operation:")
        print("1. Get all followers of an artist")
        print("2. Retrieve names and genres of artists in a follower range")
        print("3. Calculate average followers per artist")
        print("4. Search for tracks by partial name")
        print("5. Get average tracks per playlist")
        print("6. Get total likes for an artist's tracks")
        print("7. Filter and sort albums, artists, and tracks by genre")
        print("8. Exit")

        choice = input("Enter your choice (1-8): ")
        
        if choice == "1":
            identifier = input("Enter Artist ID (integer) or Name (string): ")
            if identifier.isdigit():
                identifier = int(identifier)
            followers = get_all_followers_of_artist(cursor, identifier)
            print("Followers:", followers)

        elif choice == "2":
            min_followers = int(input("Enter minimum follower count: "))
            max_followers = int(input("Enter maximum follower count: "))
            artists = get_artists_in_range(cursor, min_followers, max_followers)
            print("Artists:", artists)

        elif choice == "3":
            avg_followers = get_average_followers(cursor)
            print("Average Followers Per Artist:", avg_followers)

        elif choice == "4":
            partial_name = input("Enter partial track name: ")
            tracks = search_tracks(cursor, partial_name)
            print("Matching Tracks:", tracks)

        elif choice == "5":
            avg_tracks = get_average_tracks_per_playlist(cursor)
            print("Average Tracks Per Playlist:", avg_tracks)

        elif choice == "6":
            identifier = input("Enter Artist ID (integer) or Name (string): ")
            if identifier.isdigit():
                identifier = int(identifier)
            total_likes = get_total_likes_for_artist(cursor, identifier)
            print("Total Likes for Artist's Tracks:", total_likes)

        elif choice == "7":
            sorted_data = get_sorted_by_genre(cursor)
            print("\nArtists sorted by genre:")
            for genre, artist in sorted_data["artists"]:
                print(f"Genre: {genre}, Artist: {artist}")

            print("\nAlbums sorted by genre:")
            for genre, album in sorted_data["albums"]:
                print(f"Genre: {genre}, Album: {album}")

            print("\nTracks sorted by genre:")
            for genre, track in sorted_data["tracks"]:
                print(f"Genre: {genre}, Track: {track}")

        elif choice == "8":
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please try again.")

    cursor.close()
    db_connection.close()

if __name__ == "__main__":
    main()
