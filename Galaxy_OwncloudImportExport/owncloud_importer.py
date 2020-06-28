import argparse
import os
import sys

from logging import getLogger

from webdav3.client import Client
from webdav3.urn import Urn

import owncloud_helper as helper

log = getLogger(__name__)


def import_from_owncloud(server_url, username, password, paths):
    server_url = (server_url or os.environ.get('OWNCLOUD_SERVER_URL', '')).strip()
    username = (username or os.environ.get('OWNCLOUD_USERNAME', '')).strip()
    password = (password or os.environ.get('OWNCLOUD_PASSWORD')).strip()
    options = helper.build_connection_settings(server_url, username, password)
    client = Client(options)
    for path in paths:
        urn = Urn(path)
        create_path = path if urn.is_dir() else os.path.dirname(path)
        try:
            os.makedirs(create_path)
        except:
            pass
        client.download_sync(path, path)


def process_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('paths', type=str, nargs='+', help="Paths to import")
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
    import_from_owncloud(args.server_url, args.username, args.password,
                         args.paths)


if __name__ == "__main__":
    sys.exit(main())
