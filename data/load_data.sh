#!/usr/bin/env bash
GROUPS_DIR=./data/groups/ 
LATENCIES_DIR=./data/latencies/ 

rm -rfv $GROUPS_DIR
rm -rfv $LATENCIES_DIR
mkdir $GROUPS_DIR
mkdir $LATENCIES_DIR

CURL=$(curl 'https://darp.syntropystack.com/api/matrix' \
  -H 'authority: darp.syntropystack.com' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36' \
  -H 'content-type: application/json' \
  -H 'accept: */*' \
  -H 'origin: https://darp.syntropystack.com' \
  -H 'sec-fetch-site: same-origin' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-dest: empty' \
  -H 'referer: https://darp.syntropystack.com/' \
  -H 'accept-language: en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,lt;q=0.6,uk;q=0.5' \
  -H 'cookie: _rdt_uuid=1618254108219.2a13c493-53bc-4db2-91c7-be992831130b; _fbp=fb.1.1618254108277.764433204; __cfduid=d6ac1c630d409d8bbcff4f9867dd5f9c41618254168; _hjid=27bcc6dc-f528-4dbf-b62c-13ac922b350c; _gid=GA1.2.1979060884.1619430968; _hjTLDTest=1; ajs_user_id=%2272%22; ajs_anonymous_id=%22a34705cf-444c-4b93-9acc-718b6de38e08%22; _ga=GA1.2.722305043.1618254108; _ga_TZFDKSGXHZ=GS1.1.1619510906.7.0.1619510906.0' \
  --data-binary '{"type":"latency"}' \
  --silent \
  )

GROUPID=$(echo $CURL | grep -P '\"groupId\":\"\d+\"' -o | grep -P "\d+" -o)
LAST_GROUP_ID=$(ls -A1 $GROUPS_DIR | sort -nr | head -1 | sed -e 's/\.json$//')

if [[ $GROUPID != $LAST_GROUP_ID ]]; then
  echo "Updating Group json"
  echo $GROUPID
  echo $LAST_GROUP_ID  
  curl 'https://darp.syntropystack.com/api/nodes' \
  -X 'POST' \
  -H 'authority: darp.syntropystack.com' \
  -H 'content-length: 0' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36' \
  -H 'content-type: application/json' \
  -H 'accept: */*' \
  -H 'origin: https://darp.syntropystack.com' \
  -H 'sec-fetch-site: same-origin' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-dest: empty' \
  -H 'referer: https://darp.syntropystack.com/' \
  -H 'accept-language: en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,lt;q=0.6,uk;q=0.5' \
  -H 'cookie: _rdt_uuid=1618254108219.2a13c493-53bc-4db2-91c7-be992831130b; _fbp=fb.1.1618254108277.764433204; __cfduid=d6ac1c630d409d8bbcff4f9867dd5f9c41618254168; _hjid=27bcc6dc-f528-4dbf-b62c-13ac922b350c; _gid=GA1.2.1979060884.1619430968; _hjTLDTest=1; ajs_user_id=%2272%22; ajs_anonymous_id=%22a34705cf-444c-4b93-9acc-718b6de38e08%22; _ga=GA1.2.722305043.1618254108; _ga_TZFDKSGXHZ=GS1.1.1619510906.7.0.1619510906.0' \
  --silent \
  --compressed > $GROUPS_DIR$GROUPID-$(date +%FT%T).json
else
  echo "Already got Group JSON"
fi

echo $CURL> $LATENCIES_DIR$(date +%FT%T).json