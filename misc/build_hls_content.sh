#!/bin/bash
#
# This script generates HLS streaming content in different qualities.
# Inputs:
# $1 = input file
#

#
# Compress ans split
# $1 = input file
# $2 = size (e.g. 480x270)
#
function compress_and_split()
{
	echo "============= Compressing: $*"
	# compress and split
	ffmpeg -i $1 -map 0 -codec:v libx264 -codec:a aac -strict experimental -s $2 -f ssegment -segment_list $2.m3u8 -segment_list_flags +live -segment_time 10 ts/$2_%03d.ts
}

# remove old content if present
rm -rf ts

# create new output folder
mkdir ts

# compress and split in different resolutions
compress_and_split $1 240x130
compress_and_split $1 480x270
compress_and_split $1 640x360
compress_and_split $1 1280x720
compress_and_split $1 1920x1080

echo "============= Finish."

