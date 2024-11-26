import subprocess as sp
import pymysql
import pymysql.cursors

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
                print("1. Like a track")  
                print("2. Unlike a track") 
                print("3. Follow an artist")
                print("4. Unfollow an artist")
                print("5. Subscribe to premium")
                print("6. Unsubscribe to premium")
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