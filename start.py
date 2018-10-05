from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import yaml
import os
import json

gauth = GoogleAuth()

gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)
yaml_settings = open("settings.yaml", 'r')
yaml_settings = yaml.load(yaml_settings)

fid = yaml_settings.get('drive_folder_id')
local_dir = yaml_settings.get('directory_to_upload')
json_check = yaml_settings.get('json_check')


os.chdir(local_dir)

dir_files = os.listdir(local_dir)

print("Uploading from" + os.getcwd() + "\n\n")

print(dir_files)

print("\n\n")

try:
    with open(json_check, 'r') as ex_files:
        existing_files = json.load(ex_files)
except Exception as err:
         open(json_check, 'a').close()
         existing_files = []

uploaded_files = []


def upload_files(filename):
    if os.stat(filename).st_size <= 0 :
        return

    if os.path.isdir(filename) :
        return

    uploaded_files.append(filename)

    if filename in existing_files:
        print("Skipped " + filename)
        return


    file_1 = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": fid}]})
    #file_1.SetContentFile(os.path.join(local_dir, "", filename))
    file_1.SetContentFile(filename)
    file_1.Upload()
    print('Created file %s with mimeType %s' % (file_1['title'], file_1['mimeType']))
    with open(json_check, 'w') as outfile:
        json.dump(uploaded_files, outfile)


for file in dir_files:
    upload_files(file)
    

