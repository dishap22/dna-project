import subprocess as sp
import pymysql
import pymysql.cursors

# ============== [Functional Requirement B] ==============
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

def removeUserPlaylist(user_id, playlist_id):
    
    
    # if the user and playlist exist, remove the playlist from the user's playlists
    try:
        query = "DELETE FROM UserOwnsPlaylist WHERE User_ID = %s AND Playlist_ID = %s"
        cur.execute(query, (user_id, playlist_id))
        con.commit()

        print("Playlist removed successfully")

    except Exception as e:
        con.rollback()
        print("Failed to remove playlist")
        print(">>>>>>>>>>>>>", e)


# ============== [Functional Requirement C] ==============
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

# ============== [Functional Requirement D] ==============
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


# ============== [Functional Requirement E] ==============
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


# ============== [Functional Requirement F] ==============
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

# ============== [Functional Requirement G] ==============

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

# ============== [Functional Requirement H] ==============
def getfollowers(artist_id):
    query = "SELECT COUNT(*) FROM UserFollowsArtist WHERE Artist_ID = " + str(artist_id)
    cur.execute(query)
    followers = cur.fetchall()[0]["COUNT(*)"]
    return followers

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


# ============== [Functional Requirement I] ==============       
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




# ============== [Handler Code] ==============
def dispatch(ch):
    """
    Function that maps helper functions to option entered
    """

    if(ch == 1):
        user_id = input("Enter User ID: ")
        track_id = input("Enter Track ID: ")
        addTrackLike(user_id, track_id)
    elif(ch == 2):
        user_id = input("Enter User ID: ")
        track_id = input("Enter Track ID: ")
        removeTrackLike(user_id, track_id)
    elif(ch == 3):
        user_id = input("Enter User ID: ")
        artist_id = input("Enter Artist ID: ")
        followArtist(user_id, artist_id)
    elif(ch == 4):
        user_id = input("Enter User ID: ")
        artist_id = input("Enter Artist ID: ")
        unfollowArtist(user_id, artist_id)
    elif(ch == 5):
        user_id = input("Enter User ID: ")
        plan = input("Enter Plan: ")
        billing_date = input("Enter Billing Date: ")
        amount = input("Enter Amount: ")
        subscribeToPremium(user_id, plan, billing_date, amount)
    elif(ch == 6):
        user_id = input("Enter User ID: ")
        unsubscribeToPremium(user_id)
    elif(ch == 7):
        addplaylist()
    elif(ch == 8):
        editplaylist()
    elif (ch == 9):
        addtrack()
    elif (ch == 10):
        edittrack()
    elif (ch == 11):
        showartistanalytics()
    elif (ch == 12):
        name = input("Enter Name: ")
        email = input("Enter Email: ")
        password = input("Enter Password: ")
        is_premium = input("Is Premium (1 for Yes, 0 for No): ")
        profile_picture = input("Enter Profile Picture Path: ")

        try:
            is_premium = int(is_premium)
            if is_premium not in [0, 1]:
                raise ValueError("Is Premium must be 0 or 1.")
        except ValueError:
            print("Error: Invalid value for Is Premium. Must be 0 or 1.")
            return

        user_id = insertNewUser(name, email, password, is_premium, profile_picture)
        if user_id is None:
            return

        if is_premium == 1:
            plan = input("Enter Plan: ")
            billing_date = input("Enter Billing Date (YYYY-MM-DD): ")
            amount = input("Enter Amount to be Paid: ")
            try:
                amount = float(amount)
            except ValueError:
                print("Error: Invalid amount.")
                return
            insertPremiumUser(user_id, is_premium, plan, billing_date, amount)
    elif (ch == 13):
        user_id = input("Enter User ID: ")
        profile_picture = input("Enter New Profile Picture Path: ")
        updateProfilePicture(user_id, profile_picture)
    elif (ch == 14):
        user_id = input("Enter User ID: ")
        removeUser(user_id)
    elif (ch == 15):
        user_id = input("Enter User ID: ")
        playlist_id = input("Enter Playlist ID: ")
        removeUserPlaylist(user_id, playlist_id)
    elif (ch == 16):    
        name = input("Enter Album Name: ")
        release_date = input("Enter Release Date (YYYY-MM-DD): ")
        artist_id = input("Enter Artist ID: ")
        genre = input("Enter Genre: ")
        cover_art = input("Enter Cover Art Path: ")
        createNewAlbum(name, release_date, artist_id, genre, cover_art)
    elif (ch == 17):
        album_id = input("Enter Album ID: ")
        name = input("Enter New Album Name: ")
        release_date = input("Enter New Release Date (YYYY-MM-DD): ")
        genre = input("Enter New Genre: ")
        cover_art = input("Enter New Cover Art Path: ")
        updateAlbumDetails(album_id, name, release_date, genre, cover_art)
    else:
        print("Error: Invalid Option")


# ================= [Main Code] =================
while(1):
    tmp = sp.call('clear', shell=True)
    
    username = input("Username: ")
    password = input("Password: ")

    try:
        # Set db name accordingly which have been create by you
        # Set host to the server's address if you don't want to use local SQL server 
        con = pymysql.connect(host='localhost',
                              port=30306,
                              user="root",
                              password="password",
                              db='COMPANY',
                              cursorclass=pymysql.cursors.DictCursor)
        tmp = sp.call('clear', shell=True)

        if(con.open):
            print("Connected")
        else:
            print("Failed to connect")

        tmp = input("Enter any key to CONTINUE>")

        with con.cursor() as cur:
            while(1):
                tmp = sp.call('clear', shell=True)
                print("1. Like a track")  
                print("2. Unlike a track") 
                print("3. Follow an artist")
                print("4. Unfollow an artist")
                print("5. Subscribe to premium")
                print("6. Unsubscribe to premium")
                print("7: Add playlist")
                print("8: Edit playlist")
                print("9: Add track")
                print("10: Edit track")
                print("11: Show artist analytics")
                print("12. Insert New User")
                print("13. Update Profile Picture")
                print("14. Remove User")
                print("15. Remove Playlist from User")
                print("16. Create New Album")
                print("17. Update Album Details")
                print("18. Logout")
                ch = int(input("Enter choice> "))
                tmp = sp.call('clear', shell=True)
                if ch == 18:
                    exit()
                else:
                    dispatch(ch)
                    tmp = input("Enter any key to CONTINUE>")

    except Exception as e:
        tmp = sp.call('clear', shell=True)
        print(e)
        print("Connection Refused: Either username or password is incorrect or user doesn't have access to database")
        tmp = input("Enter any key to CONTINUE>")
