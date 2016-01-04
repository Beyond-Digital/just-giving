import requests
import json
import base64


class JustGivingAPI(object):
    apiId = None

    def __init__(self, appId):
        self.account = AccountAPIClient(appId)
        self.fundraising = FundraisingAPIClient(appId)
        # api_object.retrieve_acount


class BaseAPIClient(object):
    # 'https://api.justgiving.com' live url
    base_url = 'https://api.sandbox.justgiving.com'  # sandbox url
    api_key = None
    api_version = 'v1'
    api_endpoint = None
    authentication_code = None
    headers = None
    content_type = None

    def __init__(self, api_key, content_type='JSON'):
        self.api_key = api_key
        self.content_type = content_type
        self.set_header(content_type)

    def build_url(self):
        url = self.base_url + self.api_endpoint
        url = url.replace('[appId]', self.api_key, 1)
        url = url.replace('[apiVersion]', self.api_version, 1)
        return url

    def build_authentication(self, email, password):
        code = "{0}:{1}".format(email, password)
        self.authentication_code = base64.b64encode(code)
        self.set_header(self.content_type)

    def set_header(self, content_type):
        if content_type == 'JSON':
            content_text = 'application/json'
        else:
            content_text = 'text/xml'
        if self.authentication_code:
            headers = {'Content-Type': content_text,
                       'Authorization': 'Basic ' + self.authentication_code}
        else:
            headers = {'Content-Type': content_text}
        self.headers = headers

    def get(self):
        return requests.get(self.build_url(), headers=self.headers)

    def post(self, data):
        return requests.post(self.build_url(),
                             headers=self.headers, data=json.dumps(data))


class AccountAPIClient(BaseAPIClient):

    def get_fundraising_pages_for_user(self, email):
        self.api_endpoint = '/[appId]/[apiVersion]/account/{0}/pages'.format(
            email)
        return self.get().text

    def get_donations_for_user(self, email, password):
        self.build_authentication(email, password)
        self.api_endpoint = '/[appId]/[apiVersion]/account/donations'
        return self.get().text

    def retrieve_account(self, email, password):
        self.build_authentication(email, password)
        self.api_endpoint = '/[appId]/[apiVersion]/account'
        return self.get().text

    def validate(self, email, password):
        data = {"email": email, "password": password}
        self.api_endpoint = '/[appId]/[apiVersion]/account/validate'
        return self.post(data).text


class FundraisingAPIClient(BaseAPIClient):

    def get_fundraising_pages(self, email, password):
        self.build_authentication(email, password)
        self.api_endpoint = '/[appId]/[apiVersion]/fundraising/pages'
        return self.get().text

    def get_fundraising_page_details(self, page_short_name):
        self.api_endpoint = '/[appId]/[apiVersion]/fundraising/pages/{0}'.format(
            page_short_name)
        return self.get().text

    def get_fundraising_page_donations(self, email, password, page_short_name ):
        self.build_authentication(email, password)
        self.api_endpoint = '/[appId]/[apiVersion]/fundraising/pages/{0}/donations'.format(
            page_short_name)
        return self.get().text


if __name__ == '__main__':
    appID = '196e4994'
    j = JustGivingAPI(appID)
    # SAMPLE Check if test account exist
    print j.account.validate('ching.leung@bynd.com', 'oaktree99')
    # SAMPLE GET fundraising page
    print j.fundraising.get_fundraising_pages('ching.leung@bynd.com', 'oaktree99')
    # SAMPLE GET fundraising page deatils
    print j.fundraising.get_fundraising_page_details('byndtesting')
    # SAMPLE read donations on one particalar page
    print j.fundraising.get_fundraising_page_donations('ching.leung@bynd.com', 'oaktree99', 'byndtesting')
