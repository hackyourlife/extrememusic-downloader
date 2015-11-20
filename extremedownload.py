#!/bin/python
# vim:set ts=8 sts=8 sw=8 cc=80 tw=80 noet:

import os
import sys
import re
import json
import urllib.request

def get_page(url):
	f = urllib.request.urlopen(url)
	return f.read().decode("utf-8")

def retrieve(url, filename):
	urllib.request.urlretrieve(url, filename)

def api_call(method, extreme_env):
	url = "http%s://%s%s%s" % \
			("s" if extreme_env["API_USE_SSL"] == "yes" else "",
					extreme_env["API_HOST"],
					extreme_env["API_PATH"], method)
	authtoken = extreme_env["API_AUTH"]
	request = urllib.request.Request(url, headers={"X-API-Auth": authtoken})
	f = urllib.request.urlopen(request)
	return json.loads(f.read().decode("utf-8"))

def get_extreme_env(url):
	page = get_page(url)
	pattern = r"<script>.*?EXTREME_ENV.*?=(.*?);</script>"
	result = re.search(pattern, page)
	return json.loads(result.group(1))

def get_album(album_id, extreme_env):
	return api_call("albums/%s" % album_id, extreme_env)

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("usage: %s album-id" % sys.argv[0])
		sys.exit(1)
	album_id = sys.argv[1]
	print("ripping album id %s" % album_id)
	extreme_env = get_extreme_env("https://www.extrememusic.com")
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
			no = track["track_sound_no"]
			title = track["title"].strip()
			preview = track["assets"]["audio"]["preview_url"]
			suffix = (" (%s)" % version) \
					if version != "Full Version" else ""
			filename = "%s %s%s" % (no, title, suffix)
			filename = filename.replace("/", "-")
			print(filename)
			try:
				retrieve(preview, "%s/%s.mp3" % \
						(output_directory, filename))
			except urllib.error.HTTPError as e:
				print("%d @ URL: '%s'" % (e.code, preview))
				print("reason: '%s'" % e.reason)
				if e.code != 404:
					raise e
	except KeyboardInterrupt:
		print("download cancelled")
