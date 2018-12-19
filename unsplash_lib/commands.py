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
            instance = GetRandomPhoto(client)
        elif args.command == "search-by-keyword":
            instance = QueryImages(client, args.query, args.max_results)
        else:
            raise NotImplementedError("Command {} not implemented".format(args.command))
        #Parse post-processing args
        if args.download_folder is not None:
            instance.post_processing_command = ImagesDownload(client,args.download_folder)

        return instance

class Command:
    def __init__(self, client):
        self.client = client
    def __call__(self):
        raise NotImplementedError


class PostProcessingCommand(Command):
    """
    Postprocess results of GetCommands. Implementations of GetCommand should call set_data_to_process after execution
    """
    def __init__(self,client):
        super(PostProcessingCommand,self).__init__(client)
        self.data_to_process = None
    def set_data_to_process(self,data):
        self.data_to_process = data
    def __call__(self):
        return True

class ImagesDownload(PostProcessingCommand):
    def __init__(self, client, images_destination ='', images_format ='small'):
        """
        Download and store images in a given directory
        :param client: Unsplash Client
        :param images_destination: Directory to store images in
        :param images_format: Download images with this format. Available formats: 'raw','full','regular','small','thumb'
        """
        super(ImagesDownload, self).__init__(client)
        self.images_destination = images_destination
        self.images_format = images_format

    def __call__(self):
        assert(os.path.isdir(self.images_destination))\
            , "ERROR [ImagesDownloadCommand]: requested image destination is not a dir or does not exists"
        assert(self.images_format in ['raw','full','regular','small','thumb'])\
            ,"ERROR [ImagesDownloadCommand]: Requested format {} but format {} not supported".format(self.images_format, self.images_format)

        return self.client.download_images(self.data_to_process, self.images_destination, self.images_format)

class GetCommand(Command):
    def __init__(self, client):
        """
        GET requests to client
        :param client: Unsplash Client
        """
        super(GetCommand,self).__init__(client)

        self.request_params = {}
        self.request = ''
        self.result = None
        self.post_processing_command = PostProcessingCommand(client)

    def __call__(self):
        """
        Execute a get command, return a boolean and call an optional post_processing command on result.
        :return:
        """
        is_ok = self.execute()
        if is_ok:
            self.post_processing_command.set_data_to_process(self.result)
            self.execute_post_processing()
        return is_ok
    def execute_post_processing(self):
        return self.post_processing_command()
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
        is_ok, self.result = self.client.get(self.request, self.request_params)
        return is_ok

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

    def execute(self):
        is_ok, self.result = self.client.get_multipage_search_query(self.request, self.request_params, self.max_results)
        return is_ok
