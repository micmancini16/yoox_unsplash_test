import requests
import os
from PIL import Image
from io import BytesIO

class UnsplashClient:
    __base_api = "http://api.unsplash.com/"

    def __init__(self, access_key):
        self.authorization_header = {}
        self.authenticate(access_key)

    def authenticate(self, access_key):
        """
        Write a valid HTTP Authorization header in authorization_header.
        Some operations require only the client id, others require user authentication
        """
        raise NotImplementedError

    def get(self, request, params):

        params['Accept-Version'] = 'v1'

        res = requests.get(self.__base_api + request, params = params, headers = self.authorization_header)

        if res.status_code != 200:
            raise ConnectionError("ERROR: HTTP Status: {} : {}".format(res.status_code, [error for error in res.json()['errors']]))

        return res.json()
    def download_images(self, json_obj, destination, format):

        assert(format in ['raw','full','regular','small','thumb']),"[Client.download_images]: Requested format {} but format {} not supported".format(format,format)

        for image in json_obj:
            res = requests.get(image['urls'][format])

            if res.status_code != 200:
                raise ConnectionError(
                    "ERROR: HTTP Status: {} : {}".format(res.status_code, [error for error in res.json()['errors']]))

            img = Image.open(BytesIO(res.content))
            img.save(os.path.join(destination,image['id']+'.png'))

class PublicUnsplashClient(UnsplashClient):
    """
    This client requires only a client id. Allows public operations as queries and download on images
    """
    def __init__(self, access_key):
        super(PublicUnsplashClient,self).__init__(access_key)

    def authenticate(self, access_key):
        self.authorization_header = {'Authorization':'Client-ID {}'.format(access_key)}





