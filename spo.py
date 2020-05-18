import sqlite3
import spotipy.util as util
import spotipy
import datetime
import time


#global variables
username = ""
sp = None
cursor = None
connection = None


#all my funtions
def close():
    print("Press Enter to close..."),
    input()

def f_getUser():
    global username
    
    username = input("Username: ")


def f_close_db():
    global connection
    
    connection.commit()
    connection.close()

def f_create_tables():
    global cursor
    
    sql_command = "CREATE TABLE IF NOT EXISTS mysongs (id INTEGER PRIMARY KEY, title VARCHAR(100), interpret VARCHAR(20), urli VARCHAR(25), added DATE, added_db DATE)" # add favourite songs DB
    cursor.execute(sql_command)
    sql_command = "CREATE TABLE IF NOT EXISTS playlist (id INTEGER PRIMARY KEY, spot_id VARCHAR(30), title VARCHAR(40), follow VARCHAR(5), added_db DATE)" # add playlists DB
    cursor.execute(sql_command)
    sql_command = "CREATE TABLE IF NOT EXISTS songs_pl (id INTEGER PRIMARY KEY, title VARCHAR(100), interpret VARCHAR(20), urli VARCHAR(25), added DATE, added_db DATE)" # add playlist songs DB
    cursor.execute(sql_command)
    sql_command = "CREATE TABLE IF NOT EXISTS song_pl_connection (id INTEGER PRIMARY KEY, id_pl INTEGER, id_songs INTEGER, added_db DATE)" # add playlist song connection DB
    cursor.execute(sql_command)

def f_getSongs():
    global cursor
    
    print("Fetching your favourite songs...")
    date = str(datetime.date.today())
    i = 0
    a = 1
    while len(sp.current_user_saved_tracks(limit=50, offset=i*50)['items']) >= 50 :
        results = sp.current_user_saved_tracks(limit=50, offset=i*50)
        #print(results['items'][0]) print first "song"
        i+=1
        for item in results['items']:
            track = item['track']
            date_added = item['added_at'][:10]
            name =  track['name'].replace("'", " ")
            artist = track['artists'][0]['name'].replace("'", " ")
            sql_command = "INSERT INTO mysongs (title, interpret, urli, added, added_db) VALUES ('"+name+"', '"+artist+"', '"+track['uri'][14:]+"', "+date_added+", "+date+")"# add songs to db
            #print(sql_command)
            cursor.execute(sql_command)
            a+=1

    results = sp.current_user_saved_tracks(limit=50, offset=i*50)
    for item in results['items']:
        track = item['track']
        date_added = item['added_at'][:10]
        name =  track['name'].replace("'", " ")
        artist = track['artists'][0]['name'].replace("'", " ")
        sql_command = "INSERT INTO mysongs (title, interpret, urli, added, added_db) VALUES ('"+name+"', '"+artist+"', '"+track['uri'][14:]+"', "+date_added+", "+date+")"# add songs to db
        cursor.execute(sql_command)
        a+=1
    print("Completed! ",a-1," Songs")

def f_getPlaylists():
    global cursor
    
    print("Fetching your Playlists...\n")
    date = str(datetime.date.today())
    i = 0
    a = 1
    while len(sp.current_user_playlists(limit=50, offset=i*50)['items']) >= 50 :
        playlists = sp.current_user_playlists(limit=50, offset=i*50)
        i+=1
        for playlist in playlists['items']:
            #print(a, playlist['name'])
            name = playlist['name'].replace("'", " ")
            sql_command = "INSERT INTO playlist (spot_id, title, added_db) VALUES ('"+playlist['uri'][17:]+"', '"+name+"', '"+date+"')"# add songs to db
            cursor.execute(sql_command)
            f_getPlSongs(playlist['uri'][17:], date, name)
            a+=1
        
    playlists = sp.current_user_playlists(limit=50, offset=i*50)
    for playlist in playlists['items']:
        #print(a, playlist['name'])
        name = playlist['name'].replace("'", " ")
        sql_command = "INSERT INTO playlist (spot_id, title, added_db) VALUES ('"+playlist['uri'][17:]+"', '"+name+"', '"+date+"')"# add songs to db
        cursor.execute(sql_command)
        f_getPlSongs(playlist['uri'][17:], date, name)
        a+=1
    print("\nCompleted!",a-1,"Playlists total")
    


def f_getPlSongs(pl_id, date, pl_name):
    global cursor

    print("Adding songs to "+pl_name+" Playlist...")
    i = 0
    pltracks = sp.user_playlist_tracks(username, playlist_id=pl_id, limit=100, offset=0);
    sql_command = "SELECT id from playlist WHERE spot_id='"+pl_id+"'"# add songs to db
    cursor.execute(sql_command)
    plid = str(cursor.fetchone()[0])
    date = str(datetime.date.today())
    for item in pltracks['items']:
        i+=1
        track = item['track']
        date_added = item['added_at'][:10]
        name =  track['name'].replace("'", " ")
        artist = track['artists'][0]['name'].replace("'", " ")
        sql_command = "INSERT INTO songs_pl (title, interpret, urli, added, added_db) VALUES ('"+name+"', '"+artist+"', '"+track['uri'][14:]+"', '"+date_added+"', '"+date+"')"# add songs to db
        cursor.execute(sql_command)
        sql_command = "SELECT id from songs_pl WHERE title='"+name+"'"# add songs to db
        cursor.execute(sql_command)
        soid = str(cursor.fetchone()[0])
        sql_command = "INSERT INTO song_pl_connection (id_pl, id_songs, added_db) VALUES ('"+plid+"', '"+soid+"', '"+date+"')"
        cursor.execute(sql_command)
    print("Completed Playlist with",i,"songs!\n")
        


def main():
    global username
    print(f'Hello {username}')
    f_create_tables()
    f_getSongs()
    f_getPlaylists()
    f_close_db()
    close()

def setup():
    global sp
    global cursor
    global connection
    f_getUser()
    scope = 'user-library-read'
    token = util.prompt_for_user_token(username,scope,client_id='7168eed54b2f48a8a5d80eae42a5e31f',client_secret='6965fe3d31ba41ac8ba91ef095660833',redirect_uri='http://localhost:8888/callback/')
    sp = spotipy.Spotify(auth=token)
    connection = sqlite3.connect("spotify_"+username+".db")
    cursor = connection.cursor()

if __name__ == "__main__":
    setup()
    main()
