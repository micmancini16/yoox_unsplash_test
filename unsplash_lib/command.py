import os

class CommandFactory:
    @classmethod
    def create_command(cls, args, client):
        """

        :param args: Parsed command-line args with argparse library
        :param client: Unsplash client
        :return: Command instance
        """
        if args.command == "get-random-photo":
            return GetRandomPhoto(client)
        elif args.command == "search-by-keyword":
            return QueryImages(client, args.query, args.max_results)
        else:
            raise NotImplementedError("Command {} not implemented".format(args.command))

class Command:
    def __init__(self, client):
        self.client = client
    def execute(self):
        raise NotImplementedError

class ImagesDownloadCommand(Command):

    def __init__(self, client, images_to_be_stored_json, images_destination ='', images_format ='small'):
        """
        Download and store images in a given directory

        :param client: Unsplash Client
        :param images_to_be_stored_json: JSON data with list of images urls and metadata returned by some query
        :param images_destination: Directory to store images in
        :param images_format: Download images with this format. Available formats: 'raw','full','regular','small','thumb'
        """

        super(ImagesDownloadCommand,self).__init__(client)

        self.images_destination = images_destination
        self.images_to_be_stored_json = images_to_be_stored_json
        self.images_format = images_format

    def execute(self):
        assert(os.path.isdir(self.images_destination))\
            , "ERROR [ImagesDownloadCommand]: requested image destination is not a dir or does not exists"
        assert(self.images_format in ['raw','full','regular','small','thumb'])\
            ,"ERROR [ImagesDownloadCommand]: Requested format {} but format {} not supported".format(self.images_format, self.images_format)

        self.client.download_images(self.images_to_be_stored_json, self.images_destination, self.images_format)

class GetCommand(Command):
    def __init__(self, client):
        """
        GET requests to client
        :param client: Unsplash Client
        """
        super(GetCommand,self).__init__(client)

        self.request_params = {}
        self.request = ''
    def execute(self):
        raise NotImplementedError

class GetRandomPhoto(GetCommand):

    def __init__(self, client, count = 1):
        """
        Get a random photo from Unsplash
        :param client: Unsplash client
        :param count: Number of required images (max. 30)
        """
        super(GetRandomPhoto,self).__init__(client)
        self.request = 'photos/random'
        self.request_params = {'count': count}

    def execute(self):
        res = self.client.get(self.request, self.request_params)
        return res

class QueryImages(GetCommand):
    def __init__(self,client, query, max_results=100):
        """
        Query and return images
        :param client: Unsplash client
        :param query: Search query
        :param max_results: Maximum amount of images to be stored.
        """
        super(QueryImages,self).__init__(client)

        # max_30 elems per page supported by Unsplash API. Set to 30 to minimize calls
        elements_in_page = min(30,max_results)

        self.request = 'search/photos'
        self.request_params = {'query': query,'page':1, 'per_page': elements_in_page}
        self.max_results = max_results

    def execute(self):
        """
        Get first page and read total number of pages.
        Read following pages until required number of results is reached
        """
        #Get first page
        self.request_params['page'] = 1
        res = self.client.get(self.request, self.request_params)

        #Get number of pages
        total_pages = res['total_pages']
        total_number_of_results = res['total']

        if total_number_of_results < self.max_results:
            print("WARNING: Requested {} images but only {} images found".format(self.max_results,total_number_of_results))
            self.max_results = total_number_of_results

        image_list = res['results']

        if len(image_list) < self.max_results:
            #Get following pages until I have [max_results] images
            for page in range(2,total_pages+1):
                self.request_params['page'] = page
                res = self.client.get(self.request, self.request_params)
                for image in res['results']:
                    image_list.append(image)

                if (len(image_list) >= self.max_results):
                    break

        return image_list[:self.max_results]
