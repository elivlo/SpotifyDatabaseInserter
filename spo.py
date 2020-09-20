import msvcrt as wind
import sqlite3
import spotipy.util as util
import spotipy
import datetime
import time
import getopt, sys


class ImpVars:
    username = ""
    scope = 'user-library-read'
    
    client_id='7168eed54b2f48a8a5d80eae42a5e31f'
    client_secret='6965fe3d31ba41ac8ba91ef095660833'
    redirect_uri='http://localhost:8888/callback/'

    def __init__(self, username):
        self.username = username
        self.token = util.prompt_for_user_token(username,self.scope,client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri)
        self.sp = spotipy.Spotify(auth=self.token)

#all my funtions
def close():
    print("Press Enter to close..."),
    wind.getch()

def f_getUser():
    return input("Username: ")

def printHelp():
    print("Huhu")

def f_inputHandler():
    ###############
    optionsS = "hiou"
    optionsL = ["help", "input ", "output ", "user "]
    fullArgs = sys.argv[1:]

    try:
        arguments, values = getopt.getopt(fullArgs, optionsS, optionsL)
    except getopt.error as err:
        # output error, and return with an error code
        print (str(err))
        sys.exit(2)
    ###############
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-i", "/i"):
            print (("enabling input mode (%s)") % (currentValue))
        elif currentArgument in ("-h", "/h"):
            print ("displaying help")
        elif currentArgument in ("-o", "/o"):
            print (("enabling special output mode (%s)") % (currentValue))
        elif currentArgument in ("-u", "/u"):
            print (("username: (%s)") % (currentValue))

#def main():
    #f_create_tables()
    #f_getSongs()
    #f_getPlaylists()
    #f_close_db()

#main function
if __name__ == '__main__':
    #vm = ImpVars(f_getUser())
    f_inputHandler()
    #main()
    #close()



