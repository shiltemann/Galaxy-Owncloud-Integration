import argparse
import os
import sys
import urllib.parse

from logging import getLogger

import cachetools

from webdav3.client import Client

log = getLogger(__name__)


def upload_to_owncloud(server_url, username, password, input_file, target_path):
    server_url = (server_url or os.environ.get('OWNCLOUD_SERVER_URL')).strip()
    username = password or os.environ.get('OWNCLOUD_USERNAME')
    password = password or os.environ.get('OWNCLOUD_PASSWORD')
    options = {
        'webdav_hostname': server_url,
        'webdav_login': username,
        'webdav_password': password
    }
    client = Client(options)
    filename = os.path.basename(input_file)
    print(f"target_path: {target_path}")
    print(f"server_url: {server_url}")
    print(f"input_file: {input_file}")
    print(f"filename: {filename}")
    target_path_url = urllib.parse.urljoin(server_url, target_path)
    print(f"target_path_url: {target_path_url}")
    target_url = urllib.parse.urljoin(target_path, filename)
    print(f"target_url: {target_url}")
    client.upload(target_url, input_file)
    print(client.info(target_url))


def process_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', type=str,
                        help="File to export", required=True)
    parser.add_argument('-t', '--target_path', type=str,
                        help="Target folder location on owncloud", required=True)
    parser.add_argument('-s', '--server_url', type=str, required=False,
                        help="Webdav url of owncloud server. "
                             "e.g. https://cloudstor.aarnet.edu.au/plus/remote.php/webdav"
                             " If none, the environment variable OWNCLOUD_SERVER_URL will be respected.")
    parser.add_argument('-u', '--username', type=str, required=False,
                        help="Username for owncloud server. If not specified, the environment variable"
                             "OWNCLOUD_USERNAME will be respected.")
    parser.add_argument('-p', '--password', type=str, required=False,
                        help="Password for owncloud server. If not specified, the environment variable"
                             "OWNCLOUD_PASSWORD will be respected.")

    args = parser.parse_args(args[1:])
    return args


def main():
    args = process_args(sys.argv)
    upload_to_owncloud(args.server_url, args.username, args.password,
                       args.input_file, args.target_path)


if __name__ == "__main__":
    sys.exit(main())
