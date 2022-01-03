import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime
import sqlite3

USER_ID = '227dt3g18rrzyco2j7p2boy2ly'
TOKEN = 'BQDOWRoglEfMv0XYe89somIvBubBTAVL6JqFm-BpGxKCZMRj48JOfVlABcGtG5NBaD_UL_WP61_0fZDeaLUBSxI8vQQWzgmEptnms1wl7NTi90-cK8I56nlPVthvifi7-hD5D9xBvn1SzSjvDglTnzvNDjk6Zpj58kTkyghu'

if KeyError == True:
    print("The token has expired")
else:
    
    if __name__ == "__main__":
        
        headers = {
        "Accept":"application/json",
        "Content-Type":"application/json",
        "Authorization":"Bearer {token}".format(token=TOKEN)}
        
        r = requests.get("https://api.spotify.com/v1/me/player/recently-played",headers = headers)
        response = r.json()

        my_song_list = []

        for song in response['items']:
            artist_id = song['track']['artists'][0]['id']
            artist_name = song['track']['artists'][0]['name']
            artist_link = song['track']['artists'][0]['external_urls']['spotify'] 
            album_id = song['track']['album']['id']
            album_name = song['track']['album']['name']
            album_link = song['track']['album']['external_urls']['spotify']
            song_id = song['track']['id']
            song_name = song['track']['name']
            song_link = song['track']['external_urls']['spotify']
            duration_ms = song['track']['duration_ms']
            popularity = song['track']['popularity']
            disc_number = song['track']['disc_number']
            played_at = song['played_at'].split(".")[0]
            
            song_dic = {'artist_id': artist_id,
                            'artist_name':artist_name,
                            'artist_link':artist_link,
                            'album_id':album_id,
                            'album_name':album_name,
                            'album_link':album_link,
                            'song_id':song_id,
                            'song_name':song_name,
                            'song_link':song_link,
                            'duration_ms':duration_ms,
                            'popularity':popularity,
                            'disc_number':disc_number,
                            'played_at':played_at
                            }
            
            my_song_list.append(song_dic)
            df = pd.DataFrame(my_song_list)
            
            #Re-ordering columns in my df
            df = df[["artist_id","artist_link","album_id","album_name","album_link","song_id","song_name","song_link","duration_ms","popularity","disc_number","played_at"]]
            #Creating two columns (date, time) by spliting the played_at column.
            df[['date','time']] = df['played_at'].str.split('T',expand=True)
            #Right now, played_at, date & time are objects, so we need to change these to timestamp.
            df['date'] = pd.to_datetime(df['date'])
            df['time'] = pd.to_timedelta(df['time'])
            df['played_at'] = pd.to_datetime(df['played_at'])
            df['played_at'] = df['played_at'].dt.tz_localize('US/Central')
            ## df['played_at'] = df['played_at'].dt.strftime("%d/%m/%y")
            
            df.to_csv(r'C:\\Users\\Cesal\\projects\\spotify\\export_dataframe.csv', index = False, header = True)
            print(df)