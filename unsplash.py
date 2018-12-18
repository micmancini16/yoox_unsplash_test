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
        parser.add_argument('--max-results',type=int, help='Maximum number of returned results')

        access_key = "4a5ff7e6c98b46bdbc83bdf0d47fadfe8c797b829244978cd32ae5bbb880cbe8" #inviato via mail
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

if __name__ == '__main__':
    main()
