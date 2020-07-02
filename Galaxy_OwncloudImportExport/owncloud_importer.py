import argparse
import json
import os
import sys

from logging import getLogger

from galaxy.datatypes import sniff
from galaxy.datatypes.registry import Registry
from galaxy.util.checkers import check_binary

from webdav3.client import Client
from webdav3.urn import Urn

import owncloud_helper as helper

log = getLogger(__name__)


def download_to_path(options, paths):
    client = Client(options)
    for path in paths:
        urn = Urn(path)
        create_path = path if urn.is_dir() else os.path.dirname(path)
        try:
            os.makedirs(create_path)
        except:
            pass
        client.download_sync(path, path)


def load_datatypes_registry(job_params):
    datatypes_registry = Registry()
    datatypes_registry.load_datatypes(
        root_dir=job_params['job_config']['GALAXY_ROOT_DIR'],
        config=job_params['job_config']['GALAXY_DATATYPES_CONF_FILE'])
    return datatypes_registry


def sniff_and_handle_data_type(file_path, datatypes_registry):
    """
    The sniff.handle_uploaded_dataset_file() method in Galaxy performs dual
    functions: it sniffs the filetype and if it's a compressed archive for
    a non compressed datatype such as fasta, it will be unpacked.
    """
    ext = sniff.handle_uploaded_dataset_file(file_path, datatypes_registry)
    if not ext or ext == "data":
        is_binary = check_binary(file_path)
        ext = sniff.guess_ext(file_path, datatypes_registry.sniff_order, is_binary=is_binary)
    return ext;


def get_metadata_entry(datatypes_registry, job_params, file_path, primary_dataset=False):
    ext = sniff_and_handle_data_type(file_path, datatypes_registry)
    dataset_id = job_params['output_data'][0]['dataset_id']
    return dict(type='new_primary_dataset',
                name=os.path.basename(file_path),
                base_dataset_id=dataset_id,
                filename=file_path.lstrip("/"),
                ext=ext)


def write_metadata(metadata, paths):
    """
    Generates a new job metadata file (typically galaxy.json) with details of
    all downloaded files, which Galaxy can read and use to display history items
    and associated metadata
    """
    job_params = json.load(metadata)
    output_metadata_file = job_params['job_config']['TOOL_PROVIDED_JOB_METADATA_FILE']
    datasets_list = []
    json_output = {
        "output_file1": {
            "datasets": datasets_list
        }
    }
    with open(output_metadata_file, 'w') as json_file:
        count = 0
        datatypes_registry = load_datatypes_registry(job_params)
        for dirpath, _, filenames in os.walk("."):
            for f in filenames:
                if f == output_metadata_file:
                    continue
                abspath = os.path.join(dirpath, f)
                entry = get_metadata_entry(datatypes_registry, job_params, abspath,
                                           primary_dataset=(count == 0))
                datasets_list.append(entry)
                count += 1
        json_file.write("%s\n" % json.dumps(json_output))


def import_from_owncloud(server_url, username, password, paths, metadata):
    server_url = (server_url or os.environ.get('OWNCLOUD_SERVER_URL', '')).strip()
    username = (username or os.environ.get('OWNCLOUD_USERNAME', '')).strip()
    password = (password or os.environ.get('OWNCLOUD_PASSWORD')).strip()
    options = helper.build_connection_settings(server_url, username, password)

    download_to_path(options, paths)

    if metadata:
        write_metadata(metadata, paths)


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
    parser.add_argument('-m', '--metadata', type=argparse.FileType('r'), required=False,
                        help="Galaxy job metadata file")

    args = parser.parse_args(args[1:])
    return args


def main():
    args = process_args(sys.argv)
    import_from_owncloud(args.server_url, args.username, args.password,
                         args.paths, args.metadata)


if __name__ == "__main__":
    sys.exit(main())
