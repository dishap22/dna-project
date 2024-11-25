-- User table
CREATE TABLE User (
    User_ID INT PRIMARY KEY AUTO_INCREMENT,
    Username VARCHAR(255) UNIQUE NOT NULL,
    Email VARCHAR(255) UNIQUE NOT NULL,
    DOB DATE,
    Profile_Image BLOB,
    Password VARCHAR(255) NOT NULL,
    Is_Premium BOOLEAN DEFAULT FALSE
);

-- PremiumUsers table
CREATE TABLE PremiumUsers (
    User_ID INT PRIMARY KEY,
    Plan VARCHAR(255),
    Billing_Date DATE,
    Amount_to_Be_Paid DECIMAL(10, 2),
    -- need to add foreign key constraint and on delete cascade and on update cascade
    FOREIGN KEY (User_ID) REFERENCES User(User_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Artists table
CREATE TABLE Artists (
    Artist_ID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255) NOT NULL,
    Is_Verified BOOLEAN DEFAULT FALSE,
    Profile_Image BLOB
);

-- VerifiedArtist table
CREATE TABLE VerifiedArtist (
    Artist_ID INT PRIMARY KEY,
    Revenue_Generated DECIMAL(10, 2),
    Verification_Date DATE,
    FOREIGN KEY (Artist_ID) REFERENCES Artists(Artist_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- ArtistGenre table
CREATE TABLE ArtistGenre (
    Artist_ID INT,
    GenreName VARCHAR(255),
    PRIMARY KEY (Artist_ID, GenreName),
    FOREIGN KEY (Artist_ID) REFERENCES Artists(Artist_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- UserFollowsUser table
CREATE TABLE UserFollowsUser (
    Follower_ID INT,
    Followee_ID INT,
    PRIMARY KEY (Follower_ID, Followee_ID),
    FOREIGN KEY (Follower_ID) REFERENCES User(User_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Followee_ID) REFERENCES User(User_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- UserFollowsArtist table
CREATE TABLE UserFollowsArtist (
    User_ID INT,
    Artist_ID INT,
    PRIMARY KEY (User_ID, Artist_ID),
    FOREIGN KEY (User_ID) REFERENCES User(User_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Artist_ID) REFERENCES Artists(Artist_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Track table
CREATE TABLE Track (
    Track_ID INT PRIMARY KEY AUTO_INCREMENT,
    Track_Name VARCHAR(255) NOT NULL,
    Likes INT DEFAULT 0,
    Duration TIME,
    Streams INT DEFAULT 0,
    Album_ID INT,
    FOREIGN KEY (Album_ID) REFERENCES Albums(Album_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- TrackGenre table
CREATE TABLE TrackGenre (
    Track_ID INT,
    GenreName VARCHAR(255),
    PRIMARY KEY (Track_ID, GenreName),
    FOREIGN KEY (Track_ID) REFERENCES Track(Track_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Albums table
CREATE TABLE Albums (
    Album_ID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255) NOT NULL,
    Image BLOB,
    Release_Date DATE,
    Artist_ID INT,
    FOREIGN KEY (Artist_ID) REFERENCES Artists(Artist_ID)
);

-- Playlist table
CREATE TABLE Playlist (
    Playlist_ID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255) NOT NULL,
    Image BLOB,
    Type VARCHAR(50),
    Creator INT,
    FOREIGN KEY (Creator) REFERENCES User(User_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- PlaylistGenre table
CREATE TABLE PlaylistGenre (
    Playlist_ID INT,
    GenreName VARCHAR(255),
    PRIMARY KEY (Playlist_ID, GenreName),
    FOREIGN KEY (Playlist_ID) REFERENCES Playlist(Playlist_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- TrackInPlaylist table
CREATE TABLE TrackInPlaylist (
    Track_ID INT,
    Playlist_ID INT,
    Artist_ID INT,
    PRIMARY KEY (Track_ID, Playlist_ID),
    FOREIGN KEY (Track_ID) REFERENCES Track(Track_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Playlist_ID) REFERENCES Playlist(Playlist_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Artist_ID) REFERENCES Artists(Artist_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- ArtistsOnTrack table
CREATE TABLE ArtistsOnTrack (
    Track_ID INT,
    Artist_ID INT,
    PRIMARY KEY (Track_ID, Artist_ID),
    FOREIGN KEY (Track_ID) REFERENCES Track(Track_ID) ON DELETE CASCADE ON UPDATE CASCADE, 
    FOREIGN KEY (Artist_ID) REFERENCES Artists(Artist_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- UserLikesTrack table
CREATE TABLE UserLikesTrack (
    User_ID INT,
    Track_ID INT,
    PRIMARY KEY (User_ID, Track_ID),
    FOREIGN KEY (User_ID) REFERENCES User(User_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Track_ID) REFERENCES Track(Track_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- UserContributesToPlaylist table
CREATE TABLE UserContributesToPlaylist (
    User_ID INT,
    Playlist_ID INT,
    PRIMARY KEY (User_ID, Playlist_ID),
    FOREIGN KEY (User_ID) REFERENCES User(User_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Playlist_ID) REFERENCES Playlist(Playlist_ID) ON DELETE CASCADE ON UPDATE CASCADE
);


-- populate 
-- Populate User table
INSERT INTO User (Username, Email, DOB, Profile_Image, Password, Is_Premium) VALUES
('john_doe', 'john@example.com', '1990-01-01', 'john.png', 'password123', TRUE),
('jane_smith', 'jane@example.com', '1995-05-15', 'jane.png', 'secure456', FALSE),
('mark_brown', 'mark@example.com', '1988-08-20', NULL, 'pass789', FALSE);

-- Populate PremiumUsers table
INSERT INTO PremiumUsers (User_ID, Plan, Billing_Date, Amount_to_Be_Paid) VALUES
(1, 'Monthly', '2024-11-01', 9.99);

-- Populate Artists table
INSERT INTO Artists (Name, Is_Verified, Profile_Image) VALUES
('The Weekend', TRUE, 'weekend.png'),
('Taylor Swift', TRUE, 'taylor.png'),
('Unknown Artist', FALSE, NULL);

-- Populate VerifiedArtist table
INSERT INTO VerifiedArtist (Artist_ID, Revenue_Generated, Verification_Date) VALUES
(1, 5000000.00, '2020-01-01'),
(2, 10000000.00, '2015-06-20');

-- Populate ArtistGenre table
INSERT INTO ArtistGenre (Artist_ID, GenreName) VALUES
(1, 'Pop'),
(2, 'Country'),
(3, 'Indie');

-- Populate UserFollowsUser table
INSERT INTO UserFollowsUser (Follower_ID, Followee_ID) VALUES
(1, 2),
(2, 1),
(3, 1);

-- Populate UserFollowsArtist table
INSERT INTO UserFollowsArtist (User_ID, Artist_ID) VALUES
(1, 1),
(2, 2),
(3, 1);

-- Populate Albums table
INSERT INTO Albums (Name, Image, Release_Date, Artist_ID) VALUES
('Starboy', 'starboy.png', '2016-11-25', 1),
('1989', '1989.png', '2014-10-27', 2);

-- Populate Track table
INSERT INTO Track (Track_Name, Likes, Duration, Streams, Album_ID) VALUES
('Blinding Lights', 1000000, '00:03:20', 500000000, 1),
('Shake It Off', 2000000, '00:03:40', 1000000000, 2);

-- Populate TrackGenre table
INSERT INTO TrackGenre (Track_ID, GenreName) VALUES
(1, 'Pop'),
(2, 'Pop');

-- Populate Playlist table
INSERT INTO Playlist (Name, Image, Type, Creator) VALUES
('Morning Vibes', 'morning.png', 'Public', 1),
('Workout Mix', 'workout.png', 'Private', 2);

-- Populate PlaylistGenre table
INSERT INTO PlaylistGenre (Playlist_ID, GenreName) VALUES
(1, 'Pop'),
(2, 'Electronic');

-- Populate TrackInPlaylist table
INSERT INTO TrackInPlaylist (Track_ID, Playlist_ID, Artist_ID) VALUES
(1, 1, 1),
(2, 2, 2);

-- Populate ArtistsOnTrack table
INSERT INTO ArtistsOnTrack (Track_ID, Artist_ID) VALUES
(1, 1),
(2, 2);

-- Populate UserLikesTrack table
INSERT INTO UserLikesTrack (User_ID, Track_ID) VALUES
(1, 1),
(2, 2),
(3, 1);

-- Populate UserContributesToPlaylist table
INSERT INTO UserContributesToPlaylist (User_ID, Playlist_ID) VALUES
(1, 1),
(2, 2);