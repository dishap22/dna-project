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
            imagename = input("Enter image name: ")
            playlisttype = input("Enter playlist type (public or private): ")
            query = "INSERT INTO Playlist (Name, Image, Type, Creator) VALUES ('" + playlistname + "', '" + imagename + "', '" + playlisttype + "', " + str(rows[0]["User_ID"]) + ")"
            cur.execute(query)
            con.commit()
            print("Inserted Into Database")
        else:
            print("Incorrect password")

# edit playlist, ask to choose options between adding tracks, removing track, renaming the playlist, updating the image 



    


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
                    addplaylist()
                    # dispatch(ch)
                    # tmp = input("Enter any key to CONTINUE>")

    except Exception as e:
        #tmp = sp.call('clear', shell=True)
        print(e)
        print("Connection Refused: Either username or password is incorrect or user doesn't have access to database")
        tmp = input("Enter any key to CONTINUE>")
