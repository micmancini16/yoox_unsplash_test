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
        Write a valid HTTP Authorization header in self.authorization_header.
        Some operations require only the client id, others require user authentication
        """
        raise NotImplementedError

    def get(self, request, params):

        params['Accept-Version'] = 'v1'

        res = requests.get(self.__base_api + request, params = params, headers = self.authorization_header)

        if res.status_code != 200:
            print ("ERROR: HTTP Status: {} : {}".format(res.status_code, [error for error in res.json()['errors']]))
            return False, None

        return True, res.json()

    def get_multipage_search_query(self, request, params, max_results):
        """
        Read multiple pages of a search_query and extract [max_results] results
        """
        params['page'] = 1
        params['per_page'] = 30 #max available from APIs
        is_ok, res = self.get(request,params)
        if is_ok:
            # Get number of pages
            total_pages = res['total_pages']
            total_number_of_results = res['total']
    
            if total_number_of_results < max_results:
                print("WARNING: Requested {} items but only {} items found".format(max_results,total_number_of_results))
                max_results = total_number_of_results
    
            #init list
            items_list = res['results']
    
            if len(items_list) < max_results:
                #Get following pages until I have [max_results] images
                for page in range(1,total_pages):
                    params['page'] = page + 1 #python is 0-indexed
    
                    is_ok, res = self.get(request, params)
                    if is_ok:
                        items_list.extend(res['results'])
        
                        if (len(items_list) >= max_results):
                            break

            return is_ok, items_list[:max_results]
        else:
            return is_ok, None

    def download_images(self, json_obj, destination, format):

        print("Downloading......")
        for image in json_obj:
            res = requests.get(image['urls'][format])

            if res.status_code != 200:
                print(
                    "ERROR: HTTP Status: {} : {}".format(res.status_code, [error for error in res.json()['errors']]))
                return False
            
            img = Image.open(BytesIO(res.content))
            img.save(os.path.join(destination,image['id']+'.png'))

        print("Done.")
        return True

class PublicUnsplashClient(UnsplashClient):
    """
    This client requires only a client id. Allows public operations as queries and download on images
    """
    def __init__(self, access_key):
        super(PublicUnsplashClient,self).__init__(access_key)

    def authenticate(self, access_key):
        self.authorization_header = {'Authorization':'Client-ID {}'.format(access_key)}





