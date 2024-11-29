
# README for Phase 4 of the DNA project

## Description
This script provides functions to interact with a database, designed for a music application. 
It includes operations for managing users, artists, playlists, and tracks, along with analytical and subscription-related features.

## Commands and Functions

1. **`getAllFollowersofArtists(artist_id)`**
   - **Description**: Fetches all user IDs following a specific artist.
   ```
   def getAllFollowersofArtists(artist_id):
    try:
        query = "SELECT User_ID FROM UserFollowsArtist WHERE Artist_ID = %s"
        cur.execute(query, (artist_id,))
        result = cur.fetchall()
        if result:
            return result
        else:
            print("Error: No followers found")
            return None
    except Exception as e:
        print("Failed to retrieve followers")
        print(">>>>>>>>>>>>>", e)
        return None
   ```

2. **`getArtistsInRange(min_followers, max_followers)`**
   - **Description**: Fetches artists with followers within a specified range.
   ```
   def getArtistsInRange(min_followers,max_follower):
    try:
        query = "SELECT Artist_ID, COUNT(User_ID) AS Follower_Count FROM UserFollowsArtist GROUP BY Artist_ID HAVING COUNT(User_ID) BETWEEN %s AND %s;"
        cur.execute(query, (min_followers, max_follower))
        result = cur.fetchall()
        if result:
            return result
        else:
            print("Error: No artists found")
            return None
    except Exception as e:
        print("Failed to retrieve artists")
        print(">>>>>>>>>>>>>", e)
        return None
   ```

3. **`getAverageFollowers()`**
   - **Description**: Calculates the average number of followers for all artists.
   ```
   def getAverageFollowers():
    try:
        query = "SELECT AVG(Follower_Count) AS Average_Followers FROM ( SELECT Artist_ID, COUNT(User_ID) AS F1010ollower_Count FROM UserFollowsArtist GROUP BY Artist_ID ) AS ArtistFollowerCounts;"
        cur.execute(query)
        result = cur.fetchone()
        if result:
            return result
        else:
            print("Error: No artists found")
            return None
    except Exception as e:
        print("Failed to retrieve artists")
        print(">>>>>>>>>>>>>", e)
        return None
   ```

4. **`searchTracks(keyword)`**
   - **Description**: Searches for tracks matching the provided keyword.
   ```
   def searchTracks(search_string):
    try:
        query = "SELECT Track_ID, Track_Name FROM Track WHERE Track_Name LIKE %s"
        cur.execute(query, (f"%{search_string}%",))
        result = cur.fetchall()
        if result:
            return result
        else:
            print("Error: No tracks found")
            return None
    except Exception as e:
        print("Failed to retrieve tracks")
        print(">>>>>>>>>>>>>", e)
        return None
   ```

5. **`getAverageTracksperPlaylist()`**
   - **Description**: Computes the average number of tracks per playlist.
   ```
   def getAverageTracksperPlaylist():  
    try:
        query = "SELECT AVG(TrackCount) AS Avg_Tracks_Per_Playlist FROM (SELECT Playlist_ID, COUNT(Track_ID) AS TrackCount FROM TrackInPlaylist GROUP BY Playlist_ID) AS PlaylistTrackCounts;"
        cur.execute(query)
        result = cur.fetchone()
        if result:
            return result
        else:
            print("Error: No playlists found")
            return None
    except Exception as e:
        print("Failed to retrieve playlists")
        print(">>>>>>>>>>>>>", e)
        return None
   ```

6. **`getTotalLikesforArtist(artist_id)`**
   - **Description**: Retrieves the total number of likes for a specific artist.
   ```
   def getTotalLikesforArtist(artist_id):
    try:
        query = "SELECT a.Artist_ID, a.Name AS Artist_Name, COALESCE(SUM(t.Likes), 0) AS Total_Likes FROM Artists a JOIN Albums al ON a.Artist_ID = al.Artist_ID JOIN Track t ON al.Album_ID = t.Album_ID WHERE a.Artist_ID = %s GROUP BY a.Artist_ID, a.Name;"
        cur.execute(query, (artist_id,))
        result = cur.fetchone()
        if result:
            return result
        else:
            print("Error: No likes found")
            return None
    except Exception as e:
        print("Failed to retrieve likes")
        print(">>>>>>>>>>>>>", e)
        return None
   ```

7. **`insertNewUser(user_data)`**
   - **Description**: Inserts a new user into the database.
   ```
   def insertNewUser(name, email, password, is_premium, profile_picture):
    if name == "" or email == "" or password == "" or is_premium == "":
        print("Error: One or more fields are empty")
        return None

    try:
        query = "INSERT INTO User (Username, Email, Password, Is_Premium, Profile_Image) VALUES (%s, %s, %s, %s, %s)"
        cur.execute(query, (name, email, password, is_premium, profile_picture))
        con.commit()
        print("User inserted successfully")
    except Exception as e:
        con.rollback()
        print("Failed to insert user")
        print(">>>>>>>>>>>>>", e)
        return None
    # Obtain and return the user_id of the newly inserted user
    try:
        query = "SELECT User_ID FROM User WHERE Email = %s"
        cur.execute(query, (email,))
        user_id = cur.fetchone()['User_ID']
        print("User ID obtained successfully")
        return user_id
    except Exception as e:
        con.rollback()
        print("Failed to fetch user ID")
        print(">>>>>>>>>>>>>", e)
        return None
   ```

8. **`insertPremiumUser(user_data)`**
   - **Description**: Adds a new premium user to the database.
   ```
   def insertPremiumUser(user_id, is_premium, plan, billing_date, amount):

    if is_premium:
        try:
            query = "INSERT INTO PremiumUsers (User_ID, Plan, Billing_Date, Amount_to_Be_Paid) VALUES (%s, %s, %s, %s)"
            cur.execute(query, (user_id, plan, billing_date, amount))
            con.commit()

            print("Premium user inserted successfully")

        except Exception as e:
            con.rollback()
            print("Failed to insert premium user")
            print(">>>>>>>>>>>>>", e)
   ```

9. **`updateProfilePicture(user_id, image_url)`**
   - **Description**: Updates the profile picture for a user.
   ```
   
    def updateProfilePicture(user_id, profile_picture):
    
    # if the user exists, update their profile picture

    try:
        query = "UPDATE User SET Profile_Image = %s WHERE User_ID = %s"
        cur.execute(query, (profile_picture, user_id))
        con.commit()

        print("Profile picture updated successfully")

    except Exception as e:
        con.rollback()
        print("Failed to update profile picture")
        print(">>>>>>>>>>>>>", e)
   ```

10. **`removeUser(user_id)`**
    - **Description**: Deletes a user from the database.
    ```
    def removeUser(user_id):
    
    # if the user exists, remove them from the database
    try:
        query = "DELETE FROM User WHERE User_ID = %s"
        cur.execute(query, (user_id,))
        con.commit()

        print("User removed successfully")

    except Exception as e:
        con.rollback()
        print("Failed to remove user")
        print(">>>>>>>>>>>>>", e)
    ```

11. **`removeUserPlaylist(user_id, playlist_id)`**
    - **Description**: Deletes a playlist created by a user.
    ```
    def removeUserPlaylist(playlist_id,user_id):
    
    
    # if the user and playlist exist, remove the playlist from the user's playlists
    try:
        query = "DELETE FROM Playlist WHERE Playlist_ID = %s"
        cur.execute(query, (user_id, playlist_id))
        con.commit()

        print("Playlist removed successfully")

    except Exception as e:
        con.rollback()
        print("Failed to remove playlist")
        print(">>>>>>>>>>>>>", e)
    ```

12. **`addTrackLike(user_id, track_id)`**
    - **Description**: Adds a like to a track by a user.
    ```
        def addTrackLike(user_id, track_id):
    try: 
        query1 = "UPDATE Track SET Likes = Likes + 1 WHERE Track_ID = %s"

        query2 = "INSERT INTO UserLikesTrack (User_ID, Track_ID) VALUES (%s, %s)"
        
        cur.execute(query1, (track_id,))
        cur.execute(query2, (user_id, track_id))
        con.commit()

        print("Track liked successfully")

    except Exception as e:
        con.rollback()
        print("Failed to like the track")
        print(">>>>>>>>>>>>>", e)
    ```

13. **`removeTrackLike(user_id, track_id)`**
    - **Description**: Removes a like from a track by a user.
    ```
        def removeTrackLike(user_id, track_id):
    try: 
        query1 = "UPDATE Track SET Likes = Likes - 1 WHERE Track_ID = %s"

        query2 = "DELETE FROM UserLikesTrack WHERE User_ID = %s AND Track_ID = %s"
        
        cur.execute(query1, (track_id,))
        cur.execute(query2, (user_id, track_id))
        con.commit()

        print("Track unliked successfully")

    except Exception as e:
        con.rollback()
        print("Failed to unlike the track")
        print(">>>>>>>>>>>>>", e)
    ```

14. **`addplaylist(playlist_data)`**
    - **Description**: Creates a new playlist.
    ```
    def addplaylist():
    email = input("Enter email: ")
    query = "SELECT * FROM User WHERE Email = '" + email + "'"
    cur.execute(query)
    rows = cur.fetchall()
    con.commit()
    if len(rows) == 0:
        print("Email does not exist")
        return
    else:
        if len(rows) > 1:
            print("Multiple users with same email")
            return
        password = input("Enter password: ")
        if rows[0]["Password"] == password:
            playlistname = input("Enter playlist name: ")
            # check if playlist name already exists for same user 
            query = "SELECT * FROM Playlist WHERE Name = '" + playlistname + "' AND Creator = " + str(rows[0]["User_ID"])
            cur.execute(query)
            rows = cur.fetchall()
            con.commit()
            if len(rows) > 0:
                print("Playlist with same name already exists")
                return
            imagename = input("Enter image name: ")
            playlisttype = input("Enter playlist type (public or private): ")
            playlistgenre = input("Enter playlist genre: ")
            query = "INSERT INTO Playlist (Name, Image, Type, Creator) VALUES ('" + playlistname + "', '" + imagename + "', '" + playlisttype + "', " + str(rows[0]["User_ID"]) + ")"
            cur.execute(query)
            con.commit()
            # get playlust id of the playlist that was just added with user id and add genre to the  PlaylistGenre table
            query = "SELECT Playlist_ID FROM Playlist WHERE Name = '" + playlistname + "' AND Creator = " + str(rows[0]["User_ID"])
            cur.execute(query)
            playlistid = cur.fetchall()[0]["Playlist_ID"]
            query = "INSERT INTO PlaylistGenre (Playlist_ID, Genre) VALUES (" + str(playlistid) + ", '" + playlistgenre + "')"
            cur.execute(query)
            con.commit()
            print("Inserted Into Database")
        else:
            print("Incorrect password")
    ```

15. **`editplaylist(playlist_id, updates)`**
    - **Description**: Edits the details of an existing playlist.
    ```
    def editplaylist():
    # get user id and password
    email = input("Enter email: ")
    query = "SELECT * FROM User WHERE Email = '" + email + "'"
    cur.execute(query)
    user = cur.fetchall()
    con.commit()
    if len(user) == 0:
        print("Email does not exist")
        return
    else:
        if len(user) > 1:
            print("Multiple users with same email")
            return
        password = input("Enter password: ")
        if user[0]["Password"] != password:
            print("Incorrect password")
            return
    # get playlist name using user id
    playlistname = input("Enter playlist name: ")
    query = "SELECT Playlist_ID FROM Playlist WHERE Name = '" + playlistname + "' AND Creator = " + str(user[0]["User_ID"])
    cur.execute(query)
    playlist = cur.fetchall()
    con.commit()
    if len(playlist) == 0:
        print("Playlist does not exist")
        return
    else:
        if len(playlist) > 1:
            print("Multiple playlists with same name")
            return
        print("1. Add track")
        print("2. Remove track")
        print("3. Rename playlist")
        print("4. Update image")
        ch = int(input("Enter choice> "))
        if ch == 1:
            trackname = input("Enter track name: ")
            albumname = input("Enter album name: ")
            # get artist id
            query = "SELECT Album_ID FROM Albums WHERE Name = '" + albumname + "'"
            if cur.execute(query) == 0:
                print("Artist does not exist")
                return
            albumid = cur.fetchall()[0]["Album_ID"]
            # get track id
            query = "SELECT Track_ID FROM Track WHERE Track_Name = '" + trackname + "' AND Album_ID = " + str(albumid)
            if cur.execute(query) == 0:
                print("Track does not exist")
                return
            print("Track exists")
            trackid = cur.fetchall()[0]["Track_ID"]
            # get artist id from album id
            query = "SELECT Artist_ID FROM Albums WHERE Album_ID = " + str(albumid)
            if cur.execute(query) == 0:
                print("Artist does not exist")
                return
            artistid = cur.fetchall()[0]["Artist_ID"] 
            print("Artist ID: " + str(artistid))
            query = "INSERT INTO TrackInPlaylist (Playlist_ID, Track_ID, Artist_ID) VALUES (" + str(playlist[0]["Playlist_ID"]) + ", " + str(trackid) +  ", " + str(artistid) + ")"
            cur.execute(query)
            con.commit()
            print("Inserted Into Database")
        elif ch == 2:
            # get track id and artist id
            trackname = input("Enter track name: ")
            albumname = input("Enter album name: ")
            query = "SELECT Album_ID FROM Albums WHERE Name = '" + albumname + "'"
            if cur.execute(query) == 0:
                print("Album does not exist")
                return
            albumid = cur.fetchall()[0]["Album_ID"]
            query = "SELECT Track_ID FROM Track WHERE Track_Name = '" + trackname + "' AND Album_ID = " + str(albumid)
            if cur.execute(query) == 0:
                print("Track does not exist")
                return
            # get artist id from album id
            albumid = cur.fetchall()[0]["Album_ID"]
            query = "SELECT Artist_ID FROM Albums WHERE Album_ID = " + str(albumid)
            artistid = cur.fetchall()[0]["Artist_ID"]
            trackid = cur.fetchall()[0]["Track_ID"]
            query = "DELETE FROM TrackInPlaylist WHERE Playlist_ID = " + str(playlist[0]["Playlist_ID"]) + " AND Track_ID = " + str(trackid) + " AND Artist_ID = " + str(artistid)
            cur.execute(query)  
            con.commit()
            print("Deleted From Database")
        elif ch == 3:
            newplaylistname = input("Enter new playlist name: ")
            query = "UPDATE Playlist SET Name = '" + newplaylistname + "' WHERE Playlist_ID = " + str(playlist[0]["Playlist_ID"]) + " AND Creator = " + str(user[0]["User_ID"])
            cur.execute(query)
            con.commit()
            print("Updated In Database")
        elif ch == 4:   
            newimagename = input("Enter new image name: ")
            query = "UPDATE Playlist SET Image = '" + newimagename + "' WHERE Playlist_ID = " + str(playlist[0]["Playlist_ID"]) + " AND Creator = " + str(user[0]["User_ID"])
            cur.execute(query)
            con.commit()
            print("Updated In Database")
        else:
            print("Invalid option")
    ```

16. **`followArtist(user_id, artist_id)`**
    - **Description**: Allows a user to follow an artist.
    ```
    def followArtist(user_id, artist_id):
    try: 
        query1 = "UPDATE Artists SET Followers = Followers + 1 WHERE Artist_ID = %s"
        query2 = "INSERT INTO UserFollowsArtist (User_ID, Artist_ID) VALUES (%s, %s)"
        
        cur.execute(query1, (artist_id,))
        cur.execute(query2, (user_id, artist_id))
        con.commit()

        print("Artist followed successfully")

    except Exception as e:
        con.rollback()
        print("Failed to follow the artist")
        print(">>>>>>>>>>>>>", e)
    ```

17. **`unfollowArtist(user_id, artist_id)`**
    - **Description**: Allows a user to unfollow an artist.
    ```
    def unfollowArtist(user_id, artist_id):
    try: 
        query1 = "UPDATE Artists SET Followers = Followers - 1 WHERE Artist_ID = %s"
        query2 = "DELETE FROM UserFollowsArtist WHERE User_ID = %s AND Artist_ID = %s"
        
        cur.execute(query1, (artist_id,))
        cur.execute(query2, (user_id, artist_id))
        con.commit()

        print("Artist unfollowed successfully")

    except Exception as e:
        con.rollback()
        print("Failed to unfollow the artist")
        print(">>>>>>>>>>>>>", e)
    ```

18. **`addtrack(track_data)`**
    - **Description**: Adds a new track to the database.
    ```
    def addtrack():
    artistname = input("Enter artist name: ")
    albumname = input("Enter album name: ")
    query = "SELECT Artist_ID FROM Artist WHERE Name = '" + artistname + "'"
    if cur.execute(query) == 0:
        print("Artist does not exist")
        return
    artistid = cur.fetchall()[0]["Artist_ID"]
    query = "SELECT Album_ID FROM Albums WHERE Name = '" + albumname + "' AND Artist_ID = " + str(artistid)
    if cur.execute(query) == 0:
        print("Album does not exist")
        return
    albumid = cur.fetchall()[0]["Album_ID"]
    trackname = input("Enter track name: ")
    # also fetch track duration from user
    duration = input("Enter track duration in format HH:MM:SS : ")
    query = "INSERT INTO Track (Track_Name, Album_ID, Duration) VALUES ('" + trackname + "', " + str(albumid) + ", '" + duration + "')"
    cur.execute(query)
    con.commit()
    print("Inserted Into Database")
    ```

19. **`edittrack(track_id, updates)`**
    - **Description**: Edits the details of an existing track. Details such as the track name, track duration, track genre and the featured artist etc
    ```
    def edittrack():
    artistname = input("Enter artist name: ")
    albumname = input("Enter album name: ")
    query = "SELECT Artist_ID FROM Artist WHERE Name = '" + artistname + "'"
    if cur.execute(query) == 0:
        print("Artist does not exist")
        return
    artistid = cur.fetchall()[0]["Artist_ID"]
    query = "SELECT Album_ID FROM Albums WHERE Name = '" + albumname + "' AND Artist_ID = " + str(artistid)
    if cur.execute(query) == 0:
        print("Album does not exist")
        return
    albumid = cur.fetchall()[0]["Album_ID"]
    trackname = input("Enter track name: ")
    query = "SELECT Track_ID FROM Track WHERE Track_Name = '" + trackname + "' AND Album_ID = " + str(albumid)
    if cur.execute(query) == 0:
        print("Track does not exist")
        return
    trackid = cur.fetchall()[0]["Track_ID"]
    print("1. Edit track name")
    print("2. Edit track duration")
    print("3. Edit track genre")
    print("4. Edit featured artists")
    ch = int(input("Enter choice> "))
    if ch == 1:
        newtrackname = input("Enter new track name: ")
        query = "UPDATE Track SET Track_Name = '" + newtrackname + "' WHERE Track_ID = " + str(trackid) + " AND Album_ID = " + str(albumid)
        cur.execute(query)
        con.commit()
        print("Updated In Database")
    elif ch == 2:
        newduration = input("Enter new track duration in format HH:MM:SS : ")
        query = "UPDATE Track SET Duration = '" + newduration + "' WHERE Track_ID = " + str(trackid) + " AND Album_ID = " + str(albumid)
        cur.execute(query)
        con.commit()
        print("Updated In Database")
    elif ch == 3:
        newgenre = input("Enter new track genre: ")
        query = "UPDATE Track SET Genre = '" + newgenre + "' WHERE Track_ID = " + str(trackid) + " AND Album_ID = " + str(albumid)
        cur.execute(query)
        con.commit()
        print("Updated In Database")
    elif ch == 4:
        newfeaturedartists = input("Enter new featured artist: ")
        # check if artist exists
        query = "SELECT Artist_ID FROM Artist WHERE Name = '" + newfeaturedartists + "'"
        if cur.execute(query) == 0:
            print("Artist does not exist")
            return
        ftid = cur.fetchall()[0]["Artist_ID"]
        # Artists on track table, insert new Artist id and track id
        query = "INSERT INTO ArtistsOnTrack (Track_ID, Artist_ID) VALUES (" + str(trackid) + ", " + str(ftid) + ")"
        cur.execute(query)
        con.commit()
        print("Updated In Database")
    ```

20. **`createNewAlbum(album_data)`**
    - **Description**: Creates a new album.
    ```
    def createNewAlbum(name, release_date, artist_id, genre, cover_art):

    # if the artist exists, insert the new album

    try:
        query = "INSERT INTO Album (Name, Release_Date, Artist_ID, Genre, Cover_Art) VALUES (%s, %s, %s, %s, %s)"
        cur.execute(query, (name, release_date, artist_id, genre, cover_art))
        con.commit()

        print("Album inserted successfully")

    except Exception as e:
        con.rollback()
        print("Failed to insert album")
        print(">>>>>>>>>>>>>", e)
    ```

21. **`updateAlbumDetails(album_id, updates)`**
    - **Description**: Updates the details of an album.
    ```
    def updateAlbumDetails(album_id, name, release_date, genre, cover_art):
    

        # if the album exists, update its details
    
        try:
            query = "UPDATE Album SET Name = %s, Release_Date = %s, Genre = %s, Cover_Art = %s WHERE Album_ID = %s"
            cur.execute(query, (name, release_date, genre, cover_art, album_id))
            con.commit()
    
            print("Album details updated successfully")
    
        except Exception as e:
            con.rollback()
            print("Failed to update album details")
            print(">>>>>>>>>>>>>", e)
    ```

22. **`getfollowers(artist_id)`**
    - **Description**: Fetches the list of followers for an artist.
    ```
    def getfollowers(artist_id):
    query = "SELECT COUNT(*) FROM UserFollowsArtist WHERE Artist_ID = " + str(artist_id)
    cur.execute(query)
    followers = cur.fetchall()[0]["COUNT(*)"]
    return followers
    ```

23. **`showartistanalytics(artist_id)`**
    - **Description**: Displays analytics for a specific artist.
    ```
    def showartistanalytics():
    artistname = input("Enter artist name: ")
    query = "SELECT Artist_ID FROM Artists WHERE Name = '" + artistname + "'"
    if cur.execute(query) == 0:
        print("Artist does not exist")
        return
    artistid = cur.fetchall()[0]["Artist_ID"]
    followers = getfollowers(artistid)
    print("Followers: " + str(followers))
    query = "SELECT Track_ID FROM ArtistsOnTrack WHERE Artist_ID = " + str(artistid)
    if cur.execute(query) == 0:
        print("No tracks found")
        return
    tracks = cur.fetchall()
    total_streams = 0
    total_likes = 0
    for track in tracks:
        query = "SELECT Streams, Likes FROM Track WHERE Track_ID = " + str(track["Track_ID"])
        cur.execute(query)
        result = cur.fetchall()
        streams = result[0]["Streams"]
        likes = result[0]["Likes"]
        total_likes += likes
        total_streams += streams
    # also select the most liked and most streamed track from the artist using inner join
    query = "SELECT Track.Track_Name, Track.Streams, Track.Likes FROM Track INNER JOIN ArtistsOnTrack ON Track.Track_ID = ArtistsOnTrack.Track_ID WHERE ArtistsOnTrack.Artist_ID = " + str(artistid) + " ORDER BY Track.Streams DESC LIMIT 1"
    cur.execute(query)
    result = cur.fetchall()
    moststreamedname = result[0]["Track_Name"]
    moststreams = result[0]["Streams"]
    query = "SELECT Track.Track_Name, Track.Streams, Track.Likes FROM Track INNER JOIN ArtistsOnTrack ON Track.Track_ID = ArtistsOnTrack.Track_ID WHERE ArtistsOnTrack.Artist_ID = " + str(artistid) + " ORDER BY Track.Likes DESC LIMIT 1"
    cur.execute(query)
    result = cur.fetchall()
    mostlikedname = result[0]["Track_Name"]
    mostlikes = result[0]["Likes"]
    print("Most streamed track: " + moststreamedname + " with " + str(moststreams) + " streams")
    print("Most liked track: " + mostlikedname + " with " + str(mostlikes) + " likes")
    print("Total streams: " + str(total_streams))
    print("Total likes: " + str(total_likes))

    ```

24. **`subscribeToPremium(user_id)`**
    - **Description**: Upgrades a user to premium.
    ```
    def subscribeToPremium(user_id, plan, billing_date, amount):
    try:
        query1 = "UPDATE User SET Is_Premium = TRUE WHERE User_ID = %s"
        query2 = "INSERT INTO PremiumUsers (User_ID, Plan, Billing_Date, Amount_to_Be_Paid) VALUES (%s, %s, %s, %s)"

        cur.execute(query1, (user_id,))
        cur.execute(query2, (user_id, plan, billing_date, amount))
        con.commit()

        print("Subscribed to premium successfully")
    
    except Exception as e:
        con.rollback()
        print("Failed to subscribe to premium")
        print(">>>>>>>>>>>>>", e)
    ```

25. **`unsubscribeToPremium(user_id)`**
    - **Description**: Downgrades a user from premium.
    ```
    def unsubscribeToPremium(user_id):
    try:
        query1 = "UPDATE User SET Is_Premium = FALSE WHERE User_ID = %s"
        query2 = "DELETE FROM PremiumUsers WHERE User_ID = %s"

        cur.execute(query1, (user_id,))
        cur.execute(query2, (user_id,))
        con.commit()

        print("Unsubscribed to premium successfully")
    
    except Exception as e:
        con.rollback()
        print("Failed to unsubscribe to premium")
        print(">>>>>>>>>>>>>", e)
    ```

26. **`ArtistsSortedByGenre()`**
    - **Description**: Lists all artists sorted by genre.
    ```
    def ArtistsSortedByGenre():
    try:
        query = """
        SELECT a.Artist_ID, a.Name AS Artist_Name, ag.GenreName
        FROM Artists a
        LEFT JOIN ArtistGenre ag ON a.Artist_ID = ag.Artist_ID
        ORDER BY ag.GenreName ASC, a.Name ASC;
        """
        cur.execute(query)
        result = cur.fetchall()
        if result:
            return result
        else:
            print("Error: No artists found")
            return None
    except Exception as e:
        print("Failed to retrieve artists")
        print(">>>>>>>>>>>>>", e)
        return None
    ```

27. **`PlaylistsSortedbyGenre()`**
    - **Description**: Lists all playlists sorted by genre.
    ```
    def PlaylistsSortedbyGenre():
    try:
        query = "SELECT p.Playlist_ID, p.Name AS Playlist_Name, pg.GenreName FROM Playlist p JOIN PlaylistGenre pg ON p.Playlist_ID = pg.Playlist_ID ORDER BY pg.GenreName;"
        cur.execute(query)
        result = cur.fetchall()
        if result:
            return result
        else:
            print("Error: No albums found")
            return None
    except Exception as e:
        print("Failed to retrieve albums")
        print(">>>>>>>>>>>>>", e)
        return None
    ```

28. **`TrackssortedbyGenre()`**
    - **Description**: Lists all tracks sorted by genre.
    ```
    def TrackssortedbyGenre():
    try:
        query = "SELECT t.Track_ID, t.Track_Name, tg.GenreName FROM Track t JOIN TrackGenre tg ON t.Track_ID = tg.Track_ID ORDER BY tg.GenreName;"
        cur.execute(query)
        result = cur.fetchall()
        if result:
            return result
        else:
            print("Error: No tracks found")
            return None
    except Exception as e:
        print("Failed to retrieve tracks")
        print(">>>>>>>>>>>>>", e)
        return None
    ```

All the functions have error handling cases. There is a main function that combines all of these together and to make the application user friendly. 
