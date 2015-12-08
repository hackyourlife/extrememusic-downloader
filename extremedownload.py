#!/bin/python
# vim:set ts=8 sts=8 sw=8 cc=80 tw=80 noet:
"""
This Script can be used to Download albums and playlists from extrememusic.com
"""

import argparse
import os
import sys
import re
import json
import urllib.request

def parse_arguments():
	"""Parse command line arguments and return the list"""
	parser = argparse.ArgumentParser()
	group = parser.add_mutually_exclusive_group()
	group.add_argument("-p", "--playlist", help="Download a playlist", \
			action="store_true")
	group.add_argument("-a", "--album", \
			help="Download an album (default)", action="store_true")
	parser.add_argument("id", help="The album/playlist ID")
	return parser.parse_args()

def get_page(url):
	"""Get the page contents"""
	handle = urllib.request.urlopen(url)
	return handle.read().decode("utf-8")

def retrieve(url, filename):
	"""Download url to filename"""
	urllib.request.urlretrieve(url, filename)

def api_call(method, extreme_env):
	"""Call the API"""
	url = "http%s://%s%s%s" % \
			("s" if extreme_env["API_USE_SSL"] == "yes" else "", \
					extreme_env["API_HOST"], \
					extreme_env["API_PATH"], method)
	authtoken = extreme_env["API_AUTH"]
	request = urllib.request.Request(url, headers={"X-API-Auth": authtoken})
	handle = urllib.request.urlopen(request)
	return json.loads(handle.read().decode("utf-8"))

def get_extreme_env(url):
	"""Get the API environment variables"""
	page = get_page(url)
	pattern = r"<script>.*?EXTREME_ENV.*?=(.*?);</script>"
	result = re.search(pattern, page)
	return json.loads(result.group(1))

def is_stem(playlist_item_ids, items, track_sound_id):
	"""Returns true if version is in playlist/album"""
	for item in items:
		if item["track_sound_id"] == track_sound_id:
			item_id = item["id"]
			break
	return item_id in playlist_item_ids
	# data["playlist"]["playlist_item_ids"]

def get_album(album_id, extreme_env):
	"""Get the files related to an album"""
	return api_call("albums/%s" % album_id, extreme_env)

def get_playlist(playlist_id, extreme_env):
	"""Get the files related to a playlist"""
	return api_call("playlists/%s" % playlist_id, extreme_env)

def download_album(album_id, extreme_env):
	"""Download the files, return nothing"""
	try:
		album_id = int(sys.argv[1])
	except ValueError:
		print("id must be integer, was: '%s'" % (album_id))
		sys.exit(1)
	print("ripping album id %s" % album_id)
	album = get_album(album_id, extreme_env)
	album_title = album["album"]["title"]
	album_no = album["album"]["album_no"]
	print("album's title: %s (%s)" % (album_title, album_no))
	output_directory = "%s - %s" % (album_no, album_title)
	if not os.path.exists(output_directory):
		os.makedirs(output_directory)
	tracks = album["track_sounds"]
	try:
		for track in tracks:
			version = track["version_type"]
			number = track["track_sound_no"]
			title = track["title"].strip()
			preview = track["assets"]["audio"]["preview_url"]
			suffix = (" (%s)" % version) \
					if version != "Full Version" else ""
			filename = "%s %s%s" % (number, title, suffix)
			filename = filename.replace("/", "-")
			print(filename)
			try:
				retrieve(preview, "%s/%s.mp3" % \
						(output_directory, filename))
			except urllib.error.HTTPError as exception:
				print("%d @ URL: '%s'" % (exception.code, \
						preview))
				print("reason: '%s'" % exception.reason)
				if exception.code != 404:
					raise exception
	except KeyboardInterrupt:
		print("download cancelled")

def download_playlist(playlist_id, extreme_env):
	"""Download the files, return nothing"""
	print("ripping playlist id %s" % playlist_id)
	playlist = get_playlist(playlist_id, extreme_env)
	playlist_title = playlist["playlist"]["title"]
	print("playlist's title: %s" % (playlist_title))
	output_directory = "%s" % (playlist_title)
	if not os.path.exists(output_directory):
		os.makedirs(output_directory)
	tracks = playlist["track_sounds"]
	try:
		for track in tracks:
			version = track["version_type"]
			number = track["track_sound_no"]
			title = track["title"].strip()
			preview = track["assets"]["audio"]["preview_url"]
			suffix = (" (%s)" % version) \
					if version != "Full Version" else ""
			filename = "%s %s%s" % (number, title, suffix)
			filename = filename.replace("/", "-")
			print(filename)
			try:
				retrieve(preview, "%s/%s.mp3" % \
						(output_directory, filename))
			except urllib.error.HTTPError as exception:
				print("%d @ URL: '%s'" % (exception.code, \
						preview))
				print("reason: '%s'" % exception.reason)
				if exception.code != 404:
					raise exception
	except KeyboardInterrupt:
		print("download cancelled")

def main():
	"""The main progamm"""
	args = parse_arguments()
	extreme_env = get_extreme_env("https://www.extrememusic.com")
	if args.playlist:
		download_playlist(args.id, extreme_env)
	else:
		download_album(args.id, extreme_env)

if __name__ == "__main__":
	main()
