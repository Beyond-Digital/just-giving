import requests
import json

baseurl = 'https://api.justgiving.com'
appID = '574e1946'
headers = {'content-type': 'application/json'}
# print baseurl
r = requests.get(
    baseurl + '/' + appID + '/v1/account/mwhwong@gmail.com/pages',
    headers=headers)
# print r.headers['content-type']
# json_data = json.loads(response.text)
# print r.text


class ClientBase:

    def __init__(self):
        self.debug = false

    def build_url(self, locationFormat):
        url = locationFormat
        url = replace('{apiKey}', self.parent.apikey, url)
        url = replace('{apiVersion}', self.parent.version, url)
        return url

    def build_authentication_value(self):
    	if self.parent.username:
    		xyz = "{0}:{1}".format(self.parent.username, self.parent.password)
    		return base64.b64encode(xyz)
        return ""

    def write_line(string):
        print string


class AccountApi(ClientBase):

    def __init__(justGivingApi):
        self.parent = justGivingApi

    def account_details():
        return ""
# e_headers = {'content-type': 'application/x-www-form-urlencoded'}
# k_data = {'code': 'W3CDNKZR3NHAHLQKKCRP',
# 		  'client_secret': 'CG4XIK4TH33IZ6WISMKLGZFDA56BRYIXYQRQIUZMQWBD4BXRBK',
# 		  'client_id': '75GKPPXEUAY7HEO4SQ',
# 		  'grant_type': 'authorization_code'}

# eventbrite = requests.post(
#     'https://www.eventbrite.com/oauth/token', data=k_data, headers=e_headers)
# print eventbrite.text

# e = requests.get('https://www.eventbriteapi.com/v3/users/me/?token=KCPSXDV5PWSFJUTO4KD7')
# print e.text
