import conf
from env import ENV
from util import *

import pickle
import os.path
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import requests


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

DES = ("""
## 下載連結：
  - {download_url}
"""
)

def google_upload_file(filename, name):
    service = build('drive', 'v3', credentials=ENV.gd.creds)

    # upload file
    file_metadata = {
        'name': name,
        'parents': [ENV.gd.folder_id]
    }
    media = MediaFileUpload(
        filename,
        mimetype='application/zip',
        resumable=True
    )
    f = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    fid = f.get('id')

    return fid


def share_file(fid):
    service = build('drive', 'v3', credentials=ENV.gd.creds)
    p = {
        'type': 'anyone',
        'role': 'reader'
    }
    res = service.permissions().create(
        fileId=fid,
        body=p
    ).execute()

    url = "https://drive.google.com/uc?id={}".format(fid)
    return url

def gitlab_release(url):
    r = requests.get(
        url='https://gitlab.com/api/v4/projects/{pid}'.format(
            pid=ENV.gitlab.pid),
        headers={
            'Private-Token': ENV.gitlab.pac
        }
    )

    print(r.url)
    print(r)
    print(r.content)
    print(r.json())

    r = requests.post(
        url='https://gitlab.com/api/v4/projects/{}/releases'.format(
            ENV.gitlab.pid),
        headers={
            'Private-Token': ENV.gitlab.pac
        },
        params={
            'name': VERSION,
            'tag_name': VERSION,
            'description': DES.format(
                download_url = url
            ),
            'ref': 'master'
        }
    )

    print(r.url)
    print(r)
    print(r.content)
    print(r.json())

def main():
    name = 'ASA_HMI_Data_Agent_v{}.zip'.format(VERSION)
    filename = 'dist/{}'.format(name)
    fid = google_upload_file(filename, name)
    url = share_file(fid)
    gitlab_release(url)


if __name__ == '__main__':
    main()
