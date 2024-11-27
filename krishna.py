import subprocess as sp
import pymysql
import pymysql.cursors

# ============== [Functional Requirement B] ==============

def insertNewUser(cur, con, name, email, password, is_premium, profile_picture):
    # Check that none of the fields are empty, if they are, return None and print an error message
    if not all([name, email, password, is_premium]):
        print("Error: One or more fields are empty")
        return None

    try:
        query = "INSERT INTO User (Name, Email, Password, Is_Premium, Profile_Image) VALUES (%s, %s, %s, %s, %s)"
        cur.execute(query, (name, email, password, is_premium, profile_picture))
        con.commit()
        print("User inserted successfully")

        # Obtain and return the user_id of the newly inserted user
        query = "SELECT User_ID FROM User WHERE Email = %s"
        cur.execute(query, (email,))
        user_id = cur.fetchone()['User_ID']
        return user_id

    except Exception as e:
        con.rollback()
        print("Failed to insert user")
        print(">>>>>>>>>>>>>", e)
        return None


def insertPremiumUser(cur, con, user_id, plan, billing_date, amount):
    try:
        query = "INSERT INTO PremiumUsers (User_ID, Plan, Billing_Date, Amount_to_Be_Paid) VALUES (%s, %s, %s, %s)"
        cur.execute(query, (user_id, plan, billing_date, amount))
        con.commit()
        print("Premium user inserted successfully")
    except Exception as e:
        con.rollback()
        print("Failed to insert premium user")
        print(">>>>>>>>>>>>>", e)


def removeTrackLike(cur, con, user_id, track_id):
    try:
        query = "DELETE FROM TrackLikes WHERE User_ID = %s AND Track_ID = %s"
        cur.execute(query, (user_id, track_id))
        con.commit()
        print("Track like removed successfully")
    except Exception as e:
        con.rollback()
        print("Failed to remove track like")
        print(">>>>>>>>>>>>>", e)


def followArtist(cur, con, user_id, artist_id):
    try:
        query = "INSERT INTO ArtistFollowers (User_ID, Artist_ID) VALUES (%s, %s)"
        cur.execute(query, (user_id, artist_id))
        con.commit()
        print("Artist followed successfully")
    except Exception as e:
        con.rollback()
        print("Failed to follow artist")
        print(">>>>>>>>>>>>>", e)


def unfollowArtist(cur, con, user_id, artist_id):
    try:
        query = "DELETE FROM ArtistFollowers WHERE User_ID = %s AND Artist_ID = %s"
        cur.execute(query, (user_id, artist_id))
        con.commit()
        print("Artist unfollowed successfully")
    except Exception as e:
        con.rollback()
        print("Failed to unfollow artist")
        print(">>>>>>>>>>>>>", e)


def subscribeToPremium(cur, con, user_id, plan, billing_date, amount):
    try:
        query = "INSERT INTO PremiumUsers (User_ID, Plan, Billing_Date, Amount_to_Be_Paid) VALUES (%s, %s, %s, %s)"
        cur.execute(query, (user_id, plan, billing_date, amount))
        con.commit()
        print("Subscribed to premium successfully")
    except Exception as e:
        con.rollback()
        print("Failed to subscribe to premium")
        print(">>>>>>>>>>>>>", e)


def unsubscribeToPremium(cur, con, user_id):
    try:
        query = "DELETE FROM PremiumUsers WHERE User_ID = %s"
        cur.execute(query, (user_id,))
        con.commit()
        print("Unsubscribed from premium successfully")
    except Exception as e:
        con.rollback()
        print("Failed to unsubscribe from premium")
        print(">>>>>>>>>>>>>", e)


def dispatch(ch, cur, con):
    """
    Function that maps helper functions to option entered
    """
    if ch == 1:
        name = input("Enter Name: ")
        email = input("Enter Email: ")
        password = input("Enter Password: ")
        is_premium = int(input("Is Premium (1 for Yes, 0 for No): "))
        profile_picture = input("Enter Profile Picture URL: ")

        user_id = insertNewUser(cur, con, name, email, password, is_premium, profile_picture)
        if user_id and is_premium:
            plan = input("Enter Plan: ")
            billing_date = input("Enter Billing Date (YYYY-MM-DD): ")
            amount = float(input("Enter Amount: "))
            insertPremiumUser(cur, con, user_id, plan, billing_date, amount)

    elif ch == 2:
        user_id = input("Enter User ID: ")
        track_id = input("Enter Track ID: ")
        removeTrackLike(cur, con, user_id, track_id)

    elif ch == 3:
        user_id = input("Enter User ID: ")
        artist_id = input("Enter Artist ID: ")
        followArtist(cur, con, user_id, artist_id)

    elif ch == 4:
        user_id = input("Enter User ID: ")
        artist_id = input("Enter Artist ID: ")
        unfollowArtist(cur, con, user_id, artist_id)

    elif ch == 5:
        user_id = input("Enter User ID: ")
        plan = input("Enter Plan: ")
        billing_date = input("Enter Billing Date (YYYY-MM-DD): ")
        amount = float(input("Enter Amount: "))
        subscribeToPremium(cur, con, user_id, plan, billing_date, amount)

    elif ch == 6:
        user_id = input("Enter User ID: ")
        unsubscribeToPremium(cur, con, user_id)

    else:
        print("Error: Invalid Option")


# Main loop
while True:
    sp.call('clear', shell=True)

    try:
        con = pymysql.connect(host='localhost',
                              port=30306,
                              user="root",
                              password="password",
                              db='COMPANY',
                              cursorclass=pymysql.cursors.DictCursor)

        if con.open:
            print("Connected")
        else:
            print("Failed to connect")

        input("Enter any key to CONTINUE>")

        with con.cursor() as cur:
            while True:
                sp.call('clear', shell=True)
                print("1. Add new user")
                print("2. Unlike a track")
                print("3. Follow an artist")
                print("4. Unfollow an artist")
                print("5. Subscribe to premium")
                print("6. Unsubscribe to premium")
                print("7. Logout")
                ch = int(input("Enter choice> "))
                sp.call('clear', shell=True)
                if ch == 7:
                    exit()
                else:
                    dispatch(ch, cur, con)
                    input("Enter any key to CONTINUE>")

    except Exception as e:
        sp.call('clear', shell=True)
        print(e)
        print("Connection Refused: Check credentials or DB access")
        input("Enter any key to CONTINUE>")
