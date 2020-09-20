import sqlite3
import datetime
import time

class DataInserter:
    def __init__(self, username, sp):
        self.username = username
        self.sp = sp
        self.connection = sqlite3.connect("spotify_"+username+".db")
        self.cursor = self.connection.cursor()

    def f_close_db(self):
        self.connection.commit()
        self.connection.close()

    def f_create_tables(self):
        sql_command = "CREATE TABLE IF NOT EXISTS mysongs (id INTEGER PRIMARY KEY, title VARCHAR(100), interpret VARCHAR(20), urli VARCHAR(25), added DATE, added_db DATE)" # add favourite songs DB
        self.cursor.execute(sql_command)
        sql_command = "CREATE TABLE IF NOT EXISTS playlist (id INTEGER PRIMARY KEY, spot_id VARCHAR(30), title VARCHAR(40), follow VARCHAR(5), added_db DATE)" # add playlists DB
        self.cursor.execute(sql_command)
        sql_command = "CREATE TABLE IF NOT EXISTS songs_pl (id INTEGER PRIMARY KEY, title VARCHAR(100), interpret VARCHAR(20), urli VARCHAR(25), added DATE, added_db DATE)" # add playlist songs DB
        self.cursor.execute(sql_command)
        sql_command = "CREATE TABLE IF NOT EXISTS song_pl_connection (id INTEGER PRIMARY KEY, id_pl INTEGER, id_songs INTEGER, added_db DATE)" # add playlist song connection DB
        self.cursor.execute(sql_command)

    def f_getSongs(self):
        print("Fetching your favourite songs...")
        date = str(datetime.date.today())
        i = 0
        a = 1
        while len(self.sp.current_user_saved_tracks(limit=50, offset=i*50)['items']) >= 50 :
            results = self.sp.current_user_saved_tracks(limit=50, offset=i*50)
            #print(results['items'][0]) print first "song"
            i+=1
            for item in results['items']:
                track = item['track']
                date_added = item['added_at'][:10]
                name =  track['name'].replace("'", " ")
                artist = track['artists'][0]['name'].replace("'", " ")
                sql_command = "INSERT INTO mysongs (title, interpret, urli, added, added_db) VALUES ('"+name+"', '"+artist+"', '"+track['uri'][14:]+"', "+date_added+", "+date+")"# add songs to db
                #print(sql_command)
                self.cursor.execute(sql_command)
                a+=1

        results = self.sp.current_user_saved_tracks(limit=50, offset=i*50)
        for item in results['items']:
            track = item['track']
            date_added = item['added_at'][:10]
            name =  track['name'].replace("'", " ")
            artist = track['artists'][0]['name'].replace("'", " ")
            sql_command = "INSERT INTO mysongs (title, interpret, urli, added, added_db) VALUES ('"+name+"', '"+artist+"', '"+track['uri'][14:]+"', "+date_added+", "+date+")"# add songs to db
            self.cursor.execute(sql_command)
            a+=1
        print("Completed! ",a-1," Songs")

    def f_getPlaylists(self):
        print("Fetching your Playlists...\n")
        date = str(datetime.date.today())
        i = 0
        a = 1
        while len(self.sp.current_user_playlists(limit=50, offset=i*50)['items']) >= 50 :
            playlists = self.sp.current_user_playlists(limit=50, offset=i*50)
            i+=1
            for playlist in playlists['items']:
                #print(a, playlist['name'])
                name = playlist['name'].replace("'", " ")
                sql_command = "INSERT INTO playlist (spot_id, title, added_db) VALUES ('"+playlist['uri'][17:]+"', '"+name+"', '"+date+"')"# add songs to db
                self.cursor.execute(sql_command)
                self.f_getPlSongs(playlist['uri'][17:], date, name)
                a+=1
            
        playlists = self.sp.current_user_playlists(limit=50, offset=i*50)
        for playlist in playlists['items']:
            #print(a, playlist['name'])
            name = playlist['name'].replace("'", " ")
            sql_command = "INSERT INTO playlist (spot_id, title, added_db) VALUES ('"+playlist['uri'][17:]+"', '"+name+"', '"+date+"')"# add songs to db
            self.cursor.execute(sql_command)
            self.f_getPlSongs(playlist['uri'][17:], date, name)
            a+=1
        print("\nCompleted! ",a-1," Playlists")

    def f_getPlSongs(self, pl_id, date, pl_name):
        print("Adding songs to "+pl_name+" Playlist...")
        i = 0
        pltracks = self.sp.user_playlist_tracks(self.username, playlist_id=pl_id, limit=100, offset=0);
        sql_command = "SELECT id from playlist WHERE spot_id='"+pl_id+"'"# add songs to db
        self.cursor.execute(sql_command)
        plid = str(self.cursor.fetchone()[0])
        date = str(datetime.date.today())
        for item in pltracks['items']:
            i+=1
            track = item['track']
            date_added = item['added_at'][:10]
            name =  track['name'].replace("'", " ")
            artist = track['artists'][0]['name'].replace("'", " ")
            sql_command = "INSERT INTO songs_pl (title, interpret, urli, added, added_db) VALUES ('"+name+"', '"+artist+"', '"+track['uri'][14:]+"', '"+date_added+"', '"+date+"')"# add songs to db
            self.cursor.execute(sql_command)
            sql_command = "SELECT id from songs_pl WHERE title='"+name+"'"# add songs to db
            self.cursor.execute(sql_command)
            soid = str(self.cursor.fetchone()[0])
            sql_command = "INSERT INTO song_pl_connection (id_pl, id_songs, added_db) VALUES ('"+plid+"', '"+soid+"', '"+date+"')"
            self.cursor.execute(sql_command)
        print("Completed Playlist with ",i," songs!\n")
        