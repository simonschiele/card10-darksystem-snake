#!/bin/bash
# call like ./deploy.sh <storage_device>
# will bump revision, commit and upload to storage device

CARD_STORAGE_DEVICE="${1:-$( ls /dev/sd* | tail -n 1 )}"
CARD_REPL_DEVICE="/dev/ACM1"
MOUNTPOINT="/media/card10"

echo "Using storage device $CARD_STORAGE_DEVICE"

if [[ ! -e ${CARD_STORAGE_DEVICE} ]] ; then
	echo "Device not found" >&2
	exit 1
fi

if [[ -e ${CARD_REPL_DEVICE} ]] ; then
	echo "Device in normal/non-storage mode" >&2
	exit 1
fi

if ! sudo mount ${CARD_STORAGE_DEVICE} ${MOUNTPOINT} ; then
	echo "Couldn't mount storage device" >&2
	exit 1
fi

rev_old=$( grep -o '"revision":[0-9]*' metadata.json | cut -f2 -d':' )
rev=$(( rev_old + 1 ))
sed -i "s/revision.*/revision\":${rev}}/g" metadata.json
echo "Bumping from $rev_old to $rev"
git commit metadata.json -m "Bump $rev_old -> $rev"

if ! sudo cp -fv __init__.py metadata.json ${MOUNTPOINT}/apps/snake/ ; then
	echo "Couldn't update app files" >&2
	exit 1
fi
sync
if ! sudo umount ${MOUNTPOINT} ; then
	echo "Couldn't unmount $MOUNTPOINT" >&2
	exit 1
fi

echo "Update $rev_old -> $rev successfull"
