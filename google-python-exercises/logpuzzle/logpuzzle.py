#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib
import requests

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""


def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""
  paths = []
  file_names =[]

  with open(filename) as f:
    for line in f.readlines():
      match = re.search('GET (\S*puzzle(\S*)) HTTP', line)
      if match and not match.group(2) in file_names:
        paths.append('http://code.google.com' + match.group(1))
        file_names.append(match.group(2))

  return sorted(paths)
  

def download_images(img_urls, dest_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """

  if not os.path.exists(dest_dir):
    os.mkdir(dest_dir)

  index = open(os.path.join(dest_dir, 'index.html'), 'w')
  index.write('<html><body>\n')

  for i in range(len(img_urls)):
    # We'll be writing an HTML file to show the whole image together

    image_name = 'img{i}.jpeg'.format(i=i)

    # The w is for writing and the b is for binary because it's an image.
    # using r.headers.get('content-type') we know that all the files are jpegs
    with open(os.path.join(dest_dir, image_name), 'wb') as f:
      print('Saving {image_name}'.format(image_name=image_name))
      r = requests.get(img_urls[i])
      f.write(requests.get(img_urls[i]).content)

    index.write(f'<img src="{image_name}">'.format(image_name=image_name))

  index.write('\n</html></body>')

  index.close()

def main():
  args = sys.argv[1:]

  if not args:
    print('usage: [--todir dir] logfile ')
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])

  if todir:
    download_images(img_urls, todir)
  else:
    print('\n'.join(img_urls))

if __name__ == '__main__':
  main()
