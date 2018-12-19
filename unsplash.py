#!/usr/bin/env python

from unsplash_lib.client import PublicUnsplashClient
from unsplash_lib.commands import *
from unsplash_lib.json_viewer import JSON_Viewer

import argparse

def main():
    try:
        parser = argparse.ArgumentParser(description='Unsplash Python interface')
        parser.add_argument('command',help='Command')
        parser.add_argument('--download-folder', type=str, help='download images in this directory')
        parser.add_argument('--query', type=str, help='query images by this keyword')
        parser.add_argument('--max-results',type=int,default=100, help='Maximum number of returned results')
        parser.add_argument('--client-id',type=str,help="Client id")

        args = parser.parse_args()

        access_key = ""  # inviato via mail
        if access_key is "" and args.client_id is None:
            raise IOError("Edit code with a valid access key or provide it by command line (--client-id [access-key]).")
        elif access_key is "":
            access_key = args.client_id

        client = PublicUnsplashClient(access_key)

        command = CommandFactory.create_command(args, client)

        viewer = JSON_Viewer()

        images = command()

        if images is not None:
            viewer.print_json(images)
            if args.download_folder is not None:
               downloader = ImagesDownloadCommand(client, images, args.download_folder, images_format='small')
               downloader()

    except ConnectionError as conn_err:
        print(conn_err)
    except NotImplementedError as not_impl_err:
        print(not_impl_err)
    except IOError as io_err:
        print(io_err)
    except AssertionError as as_err:
        print(as_err)

if __name__ == '__main__':
    main()
