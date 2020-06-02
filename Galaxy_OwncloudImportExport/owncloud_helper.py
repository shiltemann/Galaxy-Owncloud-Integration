import datetime
import hashlib
from base64 import b64encode

import six

from logging import getLogger

import cachetools

from webdav3.client import Client
from webdav3.client import Urn

log = getLogger(__name__)


# Some basic Caching, so we don't have to download the entire
# directory structure every time.
CACHE_TIME = datetime.timedelta(seconds=30)
OWNCLOUD_DIRECTORIES_BY_USER = {}
RETRIEVING_OPTIONS = [{'name': 'Retrieving...', 'value': '__RETRIEVING__', 'selected': False, 'options': []}]
PATH_CONTENT_PER_USER_CACHE = cachetools.LRUCache(maxsize=128)


def recurse_folders(client, root, list_dirs_only=True):
    folders = []
    files = []
    content = []
    remote_files = client.list(root)
    # Remove first file because it's always the parent folder
    for file in remote_files[1:]:
        if Urn(file).is_dir():
            try:
               nested = recurse_folders(client, root + file, list_dirs_only=list_dirs_only)
            except:
               nested = []
            folders.append({'name': file, 'value': root + file, 'options': nested, 'selected': False})
        elif not list_dirs_only:
            files.append({'name': file, 'value': root + file, 'options': [], 'selected': False})
    # Folders and files are collected separately so folders can be listed first
    content.extend(folders)
    content.extend(files)
    return content


def hash_password(salt, password):
    return six.text_type(b64encode(
        hashlib.pbkdf2_hmac('sha256', six.text_type(password).encode(),
                            six.text_type(salt).encode(), 10000)))


def compute_hash_key(conn_settings, path, root, list_dirs_only=True, **kwargs):
    pw_hash = hash_password(conn_settings['webdav_login'], conn_settings['webdav_password'])
    return cachetools.keys.hashkey(conn_settings['webdav_hostname'],
                                   conn_settings['webdav_login'],
                                   pw_hash,
                                   path,
                                   root,
                                   list_dirs_only)


@cachetools.cached(PATH_CONTENT_PER_USER_CACHE, key=compute_hash_key)
def get_content_in_path(conn_settings, path, root, list_dirs_only=True):
    client = Client(conn_settings)
    content = []
    folders = []
    files = []
    remote_files = client.list(root)
    # Remove first file because it's always the parent folder
    for file in remote_files[1:]:
        # Retrieve only children of this path
        child_path = root + file
        if Urn(file).is_dir() and path.startswith(child_path):
            try:
               nested = get_content_in_path(conn_settings, path, child_path, list_dirs_only=list_dirs_only)
            except Exception as e:
               nested = []
            folders.append({'name': file, 'value': child_path, 'options': nested, 'selected': False, 'expanded': True})
        elif Urn(file).is_dir():
            folders.append({'name': file, 'value': child_path, 'options': RETRIEVING_OPTIONS, 'selected': False, 'expanded': False})
        elif not list_dirs_only:
            files.append({'name': file, 'value': child_path, 'options': [], 'selected': False, 'expanded': False})
    # Folders and files are collected separately so folders can be listed first
    content.extend(folders)
    content.extend(files)
    return content


def get_owncloud_folders_for_user(server_url, username, password, path="", list_dirs_only=False):
    conn_settings = {
        'webdav_hostname': server_url,
        'webdav_login': username,
        'webdav_password': password
    }
    return get_content_in_path(conn_settings, path, "", list_dirs_only=list_dirs_only)


def get_owncloud_folders(trans=None, value=None, target_folder=None, list_dirs_only=False, **kwd):
    root = ""
    if target_folder:
        if isinstance(target_folder, dict):
            root = target_folder.get('last_clicked_node') or ""

    folders = []
    if trans and trans.user:
        server_url = trans.user.extra_preferences.get('owncloud_account|server_url', "")
        username = trans.user.extra_preferences.get('owncloud_account|username', "")
        password = trans.user.extra_preferences.get('owncloud_account|password', "")

        try:
            folders = get_owncloud_folders_for_user(server_url, username, password,
                                                    path=root, list_dirs_only=list_dirs_only)
        except Exception as e:
            log.exception("Could not retrieve webdav folders: ", e)

    if not folders:
        folders = [{'name': 'Your OwnCloud username/password are incorrect or not defined', 'value': '', 'options': [], 'selected': False}]
    return folders
