import requests
import json

from manageProduct.models.instaStorage import InstaStorage


def getCreds():

    insta_storages = InstaStorage.objects.all()
    if not insta_storages.exists():
        insta_storage = InstaStorage.objects.create(access_token="EAAVMRaZBDZBOMBAFWlIXsRd50E8fX6XxNBm6ZCs0sDGjZB3fCoFxqBawT8uMzhZC7RBJ4wCn5PJ5wD3wZAv96fh2Ak8odNQqJZCaM935HwtGhv2iMQ7wZAeU7wjfuPc46kf5viTHWcaX5FlvCUQHT8VsQkiFT2eg75og2q1Y1EyWoNnP49AZCt8Lu",
                                                    account_id="17841450132501655",
                                                    app_id="1491237064669411",
                                                    app_secret="7835a3086e0dd14e2d8995255e4d26d0")
    else:
        insta_storage = insta_storages.first()

    access_token = insta_storage.access_token
    account_id = insta_storage.account_id
    app_id = insta_storage.app_id
    app_secret = insta_storage.app_secret

    creds = dict()  # dictionary to hold everything
    creds['access_token'] = access_token  # access token for use with all api calls
    creds['graph_domain'] = 'https://graph.facebook.com/'  # base domain for api calls
    creds['graph_version'] = 'v13.0'  # version of the api we are hitting
    creds['endpoint_base'] = creds['graph_domain'] + creds[
        'graph_version'] + '/'  # base endpoint with domain and version
    creds['client_id'] = app_id
    creds['client_secret'] = app_secret
    creds['instagram_account_id'] = account_id  # users instagram account id

    return creds


def makeApiCall(url, endpointParams, type):

    """ Request data from endpoint with params

    Args:
        url: string of the url endpoint to make request from
        endpointParams: dictionary keyed by the names of the url parameters
    Returns:
        object: data from the endpoint
    """

    if type == 'POST':  # post request
        data = requests.post(url, endpointParams)
    else:  # get request
        data = requests.get(url, endpointParams)

    response = dict()  # hold response info
    response['url'] = url  # url we are hitting
    response['endpoint_params'] = endpointParams  # parameters for the endpoint
    response['endpoint_params_pretty'] = json.dumps(endpointParams, indent=4)  # pretty print for cli
    response['json_data'] = json.loads(data.content)  # response data from the api
    response['json_data_pretty'] = json.dumps(response['json_data'], indent=4)  # pretty print for cli

    return response  # get and return content
