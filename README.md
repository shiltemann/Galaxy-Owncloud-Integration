# Galaxy-Owncloud-Integration

Galaxy-Owncloud integration consists of three parts:

* Owncloud App - adds "send to Galaxy" action to files in owncloud.
* Galaxy import tool - used by Owncloud app to tell Galaxy where to find its files
* Galaxy export tool - tool to send Galaxy datasets to Owncloud

### Owncloud App
Adds "send to Galaxy" action to files in owncloud. Users may then select the Galaxy server they wish to send their file to from a dropdown menu.
Configure this list in the galaxyconnect.js file.

TODO: add galaxy server from POST parameter to list of servers

### Galaxy import tool
Must be installed on the Galaxy server in order to enable the transfer of files from Owncloud to Galaxy.

### Galaxy export tool
Send files from Galaxy back to Owncloud.  
  
The default owncloud server is hardcoded here, please adjust  
The username for owncloud is assumed to be the same email address as used for galaxy registration  

CAUTION: This tool requires users to enter their owncloud password as a tool parameter. This means it will appear (base64 encoded) in the Galaxy log files. 
No output dataset is generated to avoid having the password also showing up in the users' history, but need to find better solution.. openID? Galaxy password type?


Licence (MIT)
=============

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
