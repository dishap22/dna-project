import subprocess as sp
import pymysql
import pymysql.cursors

# ============== [Functional Requirement B] ==============

def insertNewUser(name, email, password, is_premium, profile_picture):
    if name == "" or email == "" or password == "" or is_premium == "":
        print("Error: One or more fields are empty")
        return None

    try:
        query = "INSERT INTO User (Name, Email, Password, Is_Premium, Profile_Image) VALUES (%s, %s, %s, %s, %s)"
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


############################################################################################################

def dispatch(ch):
    """
    Function that maps helper functions to option entered
    """
    if ch == 1:
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

    elif ch == 2:
        user_id = input("Enter User ID: ")
        profile_picture = input("Enter New Profile Picture Path: ")
        updateProfilePicture(user_id, profile_picture)

    elif ch == 3:
        user_id = input("Enter User ID: ")
        removeUser(user_id)

    elif ch == 4:
        user_id = input("Enter User ID: ")
        playlist_id = input("Enter Playlist ID: ")
        removeUserPlaylist(user_id, playlist_id)

    elif ch == 5:
        name = input("Enter Album Name: ")
        release_date = input("Enter Release Date (YYYY-MM-DD): ")
        artist_id = input("Enter Artist ID: ")
        genre = input("Enter Genre: ")
        cover_art = input("Enter Cover Art Path: ")
        createNewAlbum(name, release_date, artist_id, genre, cover_art)

    elif ch == 6:
        album_id = input("Enter Album ID: ")
        name = input("Enter New Album Name: ")
        release_date = input("Enter New Release Date (YYYY-MM-DD): ")
        genre = input("Enter New Genre: ")
        cover_art = input("Enter New Cover Art Path: ")
        updateAlbumDetails(album_id, name, release_date, genre, cover_art)

    else:
        print("Error: Invalid Option")


# Global
while(1):
    tmp = sp.call('clear', shell=True)
    
    # Can be skipped if you want to hardcode username and password
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
                # Here taking example of Employee Mini-world
                print("1. Insert a new user")
                print("2. Update a user's profile picture")
                print("3. Remove a user")
                print("4. Remove a playlist from a user")
                print("5. Create a new album")
                print("6. Update album details")
                print("7. Logout")
                ch = int(input("Enter choice> "))
                tmp = sp.call('clear', shell=True)
                if ch == 7:
                    exit()
                else:
                    dispatch(ch)
                    tmp = input("Enter any key to CONTINUE>")

    except Exception as e:
        tmp = sp.call('clear', shell=True)
        print(e)
        print("Connection Refused: Either username or password is incorrect or user doesn't have access to database")
        tmp = input("Enter any key to CONTINUE>")
