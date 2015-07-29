
# owncloud_send.sh "$server/remote.php/webdav/$filename"  $__user_email__ $mypassb64 "$inputfile" 
filename=$1
email=$2
mypassb64=$3
mydatafile=$4

# curl -X PUT "$server/remote.php/webdav/$filename" -u $__user_email__:$mypass --data-binary @"$inputfile" 

# decode b64 encoded password
echo -n "$mypassb64" > tmpfileb64
mypass=`base64 -d tmpfileb64`

# send file to owncloud
curl -X PUT $filename -u $email:$mypass --data-binary @"$mydatafile" 