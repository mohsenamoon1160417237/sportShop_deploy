from manageProduct.instaPost.define import getCreds, makeApiCall

from manageProduct.models.instaStorage import InstaStorage


class getLongLivedAccessToken:

    def sendRequest(self, params):
        """ Get long lived access token

        API Endpoint:
            https://graph.facebook.com/{graph-api-version}/oauth/access_token?grant_type=fb_exchange_token&client_id={app-id}&client_secret={app-secret}&fb_exchange_token={your-access-token}
        Returns:
            object: data from the endpoint
        """

        endpointParams = dict()  # parameter to send to the endpoint
        endpointParams['grant_type'] = 'fb_exchange_token'  # tell facebook we want to exchange token
        endpointParams['client_id'] = params['client_id']  # client id from facebook app
        endpointParams['client_secret'] = params['client_secret']  # client secret from facebook app
        endpointParams['fb_exchange_token'] = params['access_token']  # access token to get exchange for a long lived token

        url = params['endpoint_base'] + 'oauth/access_token'  # endpoint url

        return makeApiCall(url, endpointParams, params['debug'])  # make the api call

    def doGetToken(self):

        params = getCreds()  # get creds
        params['debug'] = 'yes'  # set debug
        response = self.sendRequest(params)  # hit the api for some data!
        print("\n ---- ACCESS TOKEN INFO ----\n")  # section header
        print("Access Token:")  # label
        acc_token = response['json_data']['access_token']
        print(acc_token)
        insta_storage = InstaStorage.objects.first()
        insta_storage.access_token = acc_token
        insta_storage.save()
