### Galaxy -> Owncloud  import/export tool
Send files from Galaxy to Owncloud or fetch files from Owncloud into Galaxy.

Administrators will need to copy the sample `user_preferences_extra_conf.yml.sample` into Galaxy's config
folder and modify `user_preferences_extra_conf_path` in `galaxy.yml` to point to it. This will add some
extra fields to the Galaxy user profile so that users can select their Owncloud
server, and specify their Owncloud username/password.
