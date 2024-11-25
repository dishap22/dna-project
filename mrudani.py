import subprocess as sp
import pymysql
import pymysql.cursors

def showusers():
    #use try catch
    try:
        query = "SELECT * FROM User"
        cur.execute(query)
        rows = cur.fetchall()
        con.commit()
        #print("User ID | Username | Password")
        for row in rows:
            print(str(row["User_ID"]) + " | " + row["Username"] + " | " + row["Email"] + " | " + row["Password"]) 
        print("Inserted Into Database")
    except Exception as e:
        print(e)


# function for user to add playlist, user is required to input the playlist name, email, password, image name, type (public or private)
# make user input fields in order, one by one
# after user enters email, search in database if email exists
# if email exists, then ask user to enter password
# if password is correct, then add playlist
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

# edit playlist, ask to choose options between adding tracks, removing track, renaming the playlist, updating the image
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

# allow an artist to add tracks to a specific album, get artist name and album name first
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

# Allows artists to modify title, genre, featured artists, etc of their uploaded tracks
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


# show artist analytics, get followers, and for each album get number of streams, likes
# user innerjoin using ArtistsonTrack and use count to get number of streams

# use this
# CREATE TABLE ArtistsOnTrack (
#     Track_ID INT,
#     Artist_ID INT,
#     PRIMARY KEY (Track_ID, Artist_ID),
#     FOREIGN KEY (Track_ID) REFERENCES Track(Track_ID) ON DELETE CASCADE ON UPDATE CASCADE, 
#     FOREIGN KEY (Artist_ID) REFERENCES Artists(Artist_ID) ON DELETE CASCADE ON UPDATE CASCADE
# );

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





    


# function to get number of followers for an artist given artist id 
# use CREATE TABLE UserFollowsArtist (
#     User_ID INT,
#     Artist_ID INT,
#     PRIMARY KEY (User_ID, Artist_ID),
#     FOREIGN KEY (User_ID) REFERENCES User(User_ID) ON DELETE CASCADE ON UPDATE CASCADE,
#     FOREIGN KEY (Artist_ID) REFERENCES Artists(Artist_ID) ON DELETE CASCADE ON UPDATE CASCADE
# );

def getfollowers(artist_id):
    query = "SELECT COUNT(*) FROM UserFollowsArtist WHERE Artist_ID = " + str(artist_id)
    cur.execute(query)
    followers = cur.fetchall()[0]["COUNT(*)"]
    return followers
    








    


# Global
while(1):
    # tmp = sp.call('clear', shell=True)
    # Can be skipped if you want to hardcode username and password
    username = input("Username: ")
    password = input("Password: ")
    print("Connecting to database")
    print("Please wait")
    print(username)
    print(password)

    try:
        # Set db name accordingly which have been create by you
        # Set host to the server's address if you don't want to use local SQL server 
        con = pymysql.connect(host='localhost',
                              port=3306,
                              user=username,
                              password=password,
                              db='project',
                              cursorclass=pymysql.cursors.DictCursor)
        #tmp = sp.call('clear', shell=True)

        if(con.open):
            print("Connected")
        else:
            print("Failed to connect")

        tmp = input("Enter any key to CONTINUE>")

        with con.cursor() as cur:
            while(1):
                #tmp = sp.call('clear', shell=True)
                # Here taking example of Employee Mini-world
                print("1. Option 1")  # Hire an Employee
                print("2. Option 2")  # Fire an Employee
                print("3. Option 3")  # Promote Employee
                print("4. Option 4")  # Employee Statistics
                print("5. Logout")
                ch = int(input("Enter choice> "))
                #tmp = sp.call('clear', shell=True)
                if ch == 5:
                    exit()
                else:
                    print("helloo:)")
                    showartistanalytics()
                    # dispatch(ch)
                    # tmp = input("Enter any key to CONTINUE>")

    except Exception as e:
        #tmp = sp.call('clear', shell=True)
        print(e)
        print("Connection Refused: Either username or password is incorrect or user doesn't have access to database")
        tmp = input("Enter any key to CONTINUE>")
