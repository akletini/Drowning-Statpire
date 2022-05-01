import sqlite3
import pandas as pd
import glob, os

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = "scraper/client_secrets.json"
gauth = GoogleAuth()
gauth.LocalWebserverAuth()   
drive = GoogleDrive(gauth)

## Retrieve data from database

con = sqlite3.connect('site.db')
db_df = pd.read_sql_query("SELECT * FROM InstagramInfo", con)
db_df.to_csv("data/instagram.csv")

db_df = pd.read_sql_query("SELECT * FROM SpotifyInfo", con)
db_df.to_csv("data/spotify.csv")

db_df = pd.read_sql_query("SELECT * FROM YoutubeInfo", con)
db_df.to_csv("data/youtube.csv")

## Get root drive folder

root_folder_name = "DrowningStatpire"
folders = drive.ListFile(
    {'q': "title='" + root_folder_name + "' and mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
root_folder = drive.CreateFile(
    {
       "title" : root_folder_name,
       "mimeType" : "application/vnd.google-apps.folder",
       "id": folders[0]["id"]
    })

## Write data to drive

folder_name = "DrowningStatpireData"
folders = drive.ListFile(
    {'q': "title='" + folder_name + "' and mimeType='application/vnd.google-apps.folder' and trashed=false and '" + root_folder["id"] + "' in parents" }).GetList()

new_folder = drive.CreateFile(
    {
       "title" : folder_name,
       "mimeType" : "application/vnd.google-apps.folder",
       "parents" : [{'id': root_folder['id']}]
    })

if len(folders) == 0:
    new_folder.Upload()
else:
    old_folder = drive.CreateFile(
    {
       "title" : folder_name,
       "mimeType" : "application/vnd.google-apps.folder",
       "id": folders[0]["id"],
       "parents" : [{'id': root_folder['id']}]
    })
    old_folder.Trash()
    new_folder.Upload()


folders = drive.ListFile({'q': "title='" + folder_name + "' and mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
print(f"Created folder: {folder_name}")

for folder in folders:
    if folder['title'] == folder_name:
        for file in glob.glob("data/*.csv"):
            print(file)
            with open(file,"r") as f:
                fn = os.path.basename(f.name)
                file_drive = drive.CreateFile({'title': fn , 'parents': [{'id': folder['id']}]})  
                file_drive.SetContentString(f.read()) 
                file_drive.Upload()
                print(f"The file: {fn} has been uploaded")
