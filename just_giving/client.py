import requests
import base64


class JustGivingAPI(object):
    api_id = None

    def __init__(self, appId, sandbox=False):
        self.account = AccountAPIClient(appId, sandbox=sandbox)
        self.fundraising = FundraisingAPIClient(appId, sandbox=sandbox)


class BaseAPIClient(object):
    base_url = 'https://api.justgiving.com'
    api_key = None
    api_version = 'v1'
    api_endpoint = None
    authentication_code = None
    headers = None
    content_type = None

    def __init__(self, api_key, sandbox=False):
        self.api_key = api_key
        self.set_header()

        if sandbox:
            self.base_url = 'https://api.sandbox.justgiving.com'

    def build_url(self):
        return '{0}/{1}/{2}/{3}'.format(
            self.base_url,
            self.api_key,
            self.api_version,
            self.api_endpoint,
        )

    def build_authentication(self, email, password):
        code = "{0}:{1}".format(email, password)
        self.authentication_code = base64.b64encode(code)
        self.set_header()

    def set_header(self):
        headers = {
            'Content-Type': 'application/json',
        }
        if self.authentication_code:
            headers['Authorization'] = 'Basic ' + self.authentication_code
        self.headers = headers

    def get(self):
        response = requests.get(self.build_url(), headers=self.headers)
        response.raise_for_status()
        return response.json()

    def post(self, data):
        response = requests.post(
            self.build_url(),
            headers=self.headers,
            json=data,
        )
        response.raise_for_status()
        return response.json()

    def head(self):
        response = requests.head(self.build_url(), headers=self.headers)
        return response


class AccountAPIClient(BaseAPIClient):

    def get_fundraising_pages_for_user(self, email):
        self.api_endpoint = '/account/{0}/pages'.format(email)
        return self.get()

    def get_donations_for_user(self, email, password):
        self.build_authentication(email, password)
        self.api_endpoint = 'account/donations'
        return self.get()

    def retrieve_account(self, email, password):
        self.build_authentication(email, password)
        self.api_endpoint = 'account'
        return self.get()

    def validate(self, email, password):
        data = {"email": email, "password": password}
        self.api_endpoint = 'account/validate'
        return self.post(data)


class FundraisingAPIClient(BaseAPIClient):

    def get_fundraising_pages(self, email, password):
        self.build_authentication(email, password)
        self.api_endpoint = 'fundraising/pages'
        return self.get()

    def get_fundraising_page_details(self, page_short_name):
        self.api_endpoint = 'fundraising/pages/{0}'.format(page_short_name)
        return self.get()

    # If email and password not set, retunrs public data only
    def get_fundraising_page_donations(self, page_short_name, page_num=1, page_size=25, email=None, password=None):  # noqa
        if email and password:
            self.build_authentication(email, password)

        query_string = 'pageNum={0}&pageSize={1}'.format(page_num, page_size)
        self.api_endpoint = 'fundraising/pages/{0}/donations?{1}'.format(
            page_short_name,
            query_string,

        )
        return self.get()

    def fundraising_page_url_check(self, page_short_name):
        self.api_endpoint = 'fundraising/pages/{0}'.format(page_short_name)
        response = self.head()
        if response.status_code == 404:
            return False
        else:
            response.raise_for_status()
            return True
