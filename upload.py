from __future__ import print_function
import os
from apiclient import discovery
import oauth2client
import httplib2
from apiclient.discovery import build
from httplib2 import Http
from commands import getstatusoutput as terminal
from oauth2client import file, client, tools
import time

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.params['access_type'] = 'offline'
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

up_directory='~/Desktop/hey' #add directory address which is to be uploaded

def get_files():
    file_names=terminal('ls '+up_directory)[1].split('\n')
    if len(file_names)==1 and file_names[0]=='':
        return None
    for i in range(len(file_names)):
        terminal('cp '+up_directory+'/'+file_names[i]+' ./')
        #file_names[i]=names=os.path.join(up_directory, file_names[i])
    FILES=tuple(file_names)
    return FILES

def upload():

    FILES= get_files() #get file list and mimetype
    #return if no file to be uploaded
    if not FILES:
        return
    
    credentials=get_credentials()
    http = credentials.authorize(httplib2.Http())
    DRIVE = discovery.build('drive', 'v3', http=http)
    for filename in FILES:
        metadata = {'name': filename}
        try:
            res = DRIVE.files().create(body=metadata, media_body=filename).execute()
        except:
            continue
        if res:
            print('Uploaded "%s"' % (filename))
            terminal('rm '+filename)
            terminal('rm '+up_directory+'/'+filename)

while True:
    upload()

    delay=10 #refresh time "delay" in seconds
    time.sleep(delay)
            
