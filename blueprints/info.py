import requests
import json

class userInfo:
    def __init__(self) -> None:
        pass

    def get_google_info(google_code):
        url = 'https://www.googleapis.com/oauth2/v1/userinfo'
        headers = {'Authorization': 'Bearer ' + google_code}
        infos = requests.get(url, headers=headers)
        """
            {
            'sub': '<unique_id>',
            'name': '<full>',
            'given_name': '<first>',
            'family_name': '<last>',
            'picture': '<pic>',
            'email': '<email>',
            'email_verified': True,
            'locale': 'en'
            }
        """
        return infos.json()


    
