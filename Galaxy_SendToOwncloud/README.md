### Galaxy -> Owncloud  export tool
Send files from Galaxy to Owncloud.  
  
The default owncloud server is hardcoded here, please adjust  
The username for owncloud is assumed to be the same email address as used for galaxy registration  
  
CAUTION: This tool requires users to enter their owncloud password as a tool parameter. This means it will appear -in the clear- in the Galaxy log files. (b64 encoded to avoid accidental viewing of password by well-meaning admins, but still not secure of course)  
No output dataset is generated to avoid having the password also show up in the users' history, but need to find better solution.. openID? galaxy password param type?
