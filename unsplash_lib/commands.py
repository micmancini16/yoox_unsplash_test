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
    def __call__(self):
        raise NotImplementedError

class ImagesDownloadCommand(Command):

    def __init__(self, client, images_to_be_stored_json, images_destination ='', images_format ='small'):
        """
        Download and store images in a given directory

        :param client: Unsplash Client
        :param images_to_be_stored_json: JSON data with list of images urls and metadata as returned by some query
        :param images_destination: Directory to store images in
        :param images_format: Download images with this format. Available formats: 'raw','full','regular','small','thumb'
        """

        super(ImagesDownloadCommand,self).__init__(client)

        self.images_destination = images_destination
        self.images_to_be_stored_json = images_to_be_stored_json
        self.images_format = images_format

    def __call__(self):
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
    def __call__(self):
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

    def __call__(self):
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

        self.request = 'search/photos'
        self.request_params = {'query': query}
        self.max_results = max_results

    def __call__(self):
        res = self.client.get_multipage_search_query(self.request, self.request_params, self.max_results)
        return res
