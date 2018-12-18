#!/usr/bin/env python

from unsplash_lib.client import PublicUnsplashClient
from unsplash_lib.command import *
from unsplash_lib.json_viewer import JSON_Viewer

import argparse

def main():
    try:
        parser = argparse.ArgumentParser(description='Unsplash Python interface')
        parser.add_argument('command',help='Command')
        parser.add_argument('--download-folder', type=str, help='download images in this directory')
        parser.add_argument('--query', type=str, help='query images by this keyword')
        parser.add_argument('--max-results',type=int,default=100, help='Maximum number of returned results')

        access_key = "" #inviato via mail
        if access_key is "":
            raise IOError("Edit code with a valid access key.")
        client = PublicUnsplashClient(access_key)

        args = parser.parse_args()
        command = CommandFactory.create_command(args, client)

        viewer = JSON_Viewer()

        images = command.execute()

        if images is not None:
            viewer.print_json(images)
            if args.download_folder is not None:
               downloader = ImagesDownloadCommand(client, images, args.download_folder)
               downloader.execute()

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
