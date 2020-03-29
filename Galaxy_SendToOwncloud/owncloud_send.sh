# owncloud_send.sh "$server/remote.php/webdav/$filename"  $__user_email__ $mypassb64 "$inputfile"
server_url=$1
username_b64=$2
password_b64=$3
mydatafile=$4
filename_b64=$5

username=$(echo $username_b64 | base64 --decode)
password=$(echo $password_b64 | base64 --decode)
filename=$(echo $filename_b64 | base64 --decode)

echo curl -X PUT $server_url/$username/$filename -u $username:$password --data-binary @"$mydatafile" > /tmp/owncloud.txt
# send file to owncloud
curl -X PUT $server_url/$username/$filename -u $username:$password --data-binary @"$mydatafile"
