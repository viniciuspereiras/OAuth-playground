import os
from dotenv import load_dotenv
import random 
import hashlib
import requests
import pdb
load_dotenv('../.env')

google_client_id = os.getenv('GOOGLE_CLIENT_ID')
google_client_secret = os.getenv('GOOGLE_CLIENT_SECRET')

class Authentication:
    def __init__(self):
        self.google_state = None
        pass

    def check(session):
        try:
            if session["logged_in"] == None or session["logged_in"] == False:
                return False
            else:
                return True
        except KeyError:
            return False

    def authGoogle():
        scope = ['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile']

        #generate random md5 string for state
        state = hashlib.md5(str(random.getrandbits(256)).encode('utf-8')).hexdigest()
        google_url = f'https://accounts.google.com/o/oauth2/v2/auth?scope={"%20".join(scope)}&redirect_uri=http://localhost:5000/auth/google/callback&response_type=code&client_id={google_client_id}&state={state}'
        
        return {
            'google_url': google_url,
            'state': state
        }

    def getGoogleToken(code):
        """
            {
            "access_token": "xxxxxxxxxxxxxxx",
            "expires_in": 3920,
            "token_type": "Bearer",
            "scope": "https://www.googleapis.com/auth/drive.metadata.readonly",
            "refresh_token": "xxxxxxxxxxxxxxxxxxxxx"
            }
        """
        
        
        data = {
            'code': code,
            'client_id': google_client_id,
            'client_secret': google_client_secret,
            'redirect_uri': 'http://localhost:5000/auth/google/callback',
            'grant_type': 'authorization_code'
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post('https://oauth2.googleapis.com/token', data=data, headers=headers)
        return response.json()
