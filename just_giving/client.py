import requests
import base64


class JustGivingAPI(object):
    apiId = None

    def __init__(self, appId):
        self.account = AccountAPIClient(appId)
        self.fundraising = FundraisingAPIClient(appId)
        # api_object.retrieve_acount


class BaseAPIClient(object):
    base_url = 'https://api.justgiving.com/'  # live url
    # base_url = 'https://api.sandbox.justgiving.com'  # sandbox url
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
        return '{0}/{1}/{2}/{3}'.format(
            self.base_url,
            self.api_key,
            self.api_version,
            self.api_endpoint,
        )

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
            headers = {
                'Content-Type': content_text,
                'Authorization': 'Basic ' + self.authentication_code
            }
        else:
            headers = {'Content-Type': content_text}
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
        return requests.head(self.build_url(), headers=self.headers)


class AccountAPIClient(BaseAPIClient):

    def get_fundraising_pages_for_user(self, email):
        self.api_endpoint = '/account/{0}/pages'.format(
            email)
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
        self.api_endpoint = 'fundraising/pages/{0}'.format(
            page_short_name)
        return self.get()

    # If email and password not set, retunrs public data only
    def get_fundraising_page_donations(self, page_short_name, page_num=1, page_size=25, email=None, password=None):
        if email and password:
            self.build_authentication(email, password)

        self.api_endpoint = 'fundraising/pages/{0}/donations?pageNum={1}&pageSize={2}'.format(
            page_short_name, page_num, page_size)
        return self.get()

    def fundraising_page_url_check(self, page_short_name):
        self.api_endpoint = 'fundraising/pages/{0}'.format(
            page_short_name)
        return self.head()

if __name__ == '__main__':
    from pprint import pprint
    appID = '196e4994'
    j = JustGivingAPI(appID)
    # SAMPLE Check if test account exist
    print j.account.validate('ching.leung@bynd.com', 'oaktree99')
    # SAMPLE GET fundraising page
    # print j.fundraising.get_fundraising_pages('ching.leung@bynd.com', 'oaktree99')
    # SAMPLE GET fundraising page deatils
    #pprint(j.fundraising.get_fundraising_page_details('Nicholas-Jones16'))
    # SAMPLE read donations on one particalar page, with page size of 150
    # result
    #print j.fundraising.get_fundraising_page_donations('Nicholas-Jones16', 1, 150)
    # Check if justgiving donation page exist
    # print j.fundraising.fundraising_page_url_check('micwong')
