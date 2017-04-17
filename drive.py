from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from datetime import datetime
import os
import glob
import json
import subprocess


class gDrive():

    def __init__(self):
        gauth = GoogleAuth()
        if os.path.isfile('Credentials.txt') == False:
            open('./Credentials.txt', 'w+')
        gauth.LoadCredentialsFile("Credentials.txt")
        if gauth.credentials is None:
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            print "Google Drive Token Expired, Refreshing"
            gauth.Refresh()
        else:
            gauth.Authorize()
        gauth.SaveCredentialsFile("Credentials.txt")
        self.drive = GoogleDrive(gauth)

    def uploadFile(self, file_path, file_name, folder_id=False):
        option = {'title': str(file_name)}
        if folder_id:
            option = {'title': str(file_name), "parents":  [
                {"id": str(folder_id)}]}
        file = self.drive.CreateFile(option)
        file.SetContentFile(file_path)
        file.Upload()
        return file

    def getAll(self):
        folder_list = self.drive.ListFile(
            {'q': "mimeType='application/vnd.google-apps.folder'"}).GetList()
        for folder in folder_list:
            print '\n %s folder(%s) shared status %s' % (
                folder.get('title'),
                folder.get('id'),
                folder.get('shared'))
            query = "trashed = false and '%s' in parents" % (folder.get('id'))

            file_list = self.drive.ListFile({'q': query}).GetList()
            for file1 in file_list:
                print '\n File title: %s, id: %s' % (
                    file1['title'],
                    file1['id'],
                )

    def process(self):
        os.system("echo 'start upload to google drive'")
        file_path, file_name = self.exportPsqlData()
        self.uploadFile(file_path, file_name)
        os.remove(file_path)
        os.system("echo 'upload done'")

    def exportPsqlData(self):
        dbname = 'db_name'
        user = 'your system user'
        file_name = dbname + '-' + datetime.now().strftime("%d-%m-%y") + '.sql.gz'
        file_path = '/tmp/' + file_name

        os.system(("pg_dump -U %s %s | gzip -9 > %s") %
                  (user, dbname, file_path))
        return file_path, file_name

gDrive().getAll()
