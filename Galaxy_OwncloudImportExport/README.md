### Galaxy -> Owncloud  import/export tool
Send files from Galaxy to Owncloud or fetch files from Owncloud into Galaxy.

Administrators will need to copy the sample `user_preferences_extra_conf.yml.sample` into Galaxy's config
folder and modify `user_preferences_extra_conf_path` in `galaxy.yml` to point to it. This will add some
extra fields to the Galaxy user profile so that users can select their Owncloud
server, and specify their Owncloud username/password.
  
  
CAUTION: This tool requires users to enter their owncloud password as a tool parameter. This means it will appear -in the clear- in the Galaxy log files. (b64 encoded to avoid accidental viewing of password by well-meaning admins, but still not secure of course)  
No output dataset is generated to avoid having the password also show up in the users' history, but need to find better solution.. openID? galaxy password param type?
