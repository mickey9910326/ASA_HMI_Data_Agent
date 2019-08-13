from configparser import ConfigParser

from google_auth_oauthlib.flow import InstalledAppFlow
import google.oauth2.credentials
import pickle
import os

__all__ = ['ENV']

class Env(object):
    """docstring for Env."""

    class _Gitlab(object):
        pid = str()
        pac = str() # personal access token

    class _GD(object):
        """para for google driver"""
        _cred_file = str()
        _pickle_file = str()
        folder_id = str()
        creds = object()

    gitlab = _Gitlab()
    gd = _GD()

    def __init__(self, file):
        super(Env, self).__init__()
        self.env_paser(file)
    
    def env_paser(self, file):
        cfg = ConfigParser()
        cfg.read(file)
        self.gitlab.pid = cfg['gitlab']['pid']
        self.gitlab.pac = cfg['gitlab']['pac']
        self.gd._cred_file = cfg['google']['cred_file']
        self.gd._pickle_file = cfg['google']['pickle_file']
        self.gd.folder_id = cfg['google']['folder_id']
        self.gd.creds = self.get_google_auth()
    
    def get_google_auth(self):
        scopes = ['https://www.googleapis.com/auth/drive']

        if os.path.exists(self.gd._cred_file):
            with open(self.gd._pickle_file, 'rb') as token:
                creds = pickle.load(token)
        
        # If there are no (valid) credentials available,
        # let the user log in.
        if not creds or not creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file(
                self.gd._cred_file, scopes
            )
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(self.gd._pickle_file, 'wb') as token:
            pickle.dump(creds, token)
        
        return creds
        
ENV = Env('env/.env')

if __name__ == "__main__":
    # TODO put this to test
    print(ENV.gitlab.pid)
    print(ENV.gitlab.pac)
    print(ENV.gd._cred_file)
    print(ENV.gd._pickle_file)
    print(ENV.gd.folder_id)
    print(ENV.gd.creds)
