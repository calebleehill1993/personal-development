#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
import subprocess

"""Copy Special exercise
"""

def get_special_paths(dir):
  """Gets all of the special paths in a given directory.
  :param dir Given directory to look through
  :returns list of absolute paths"""
  absolute_paths = []
  for filename in os.listdir(dir):
    match = re.search(r'__\w+__', filename)
    if match:
      absolute_paths.append(os.path.abspath(filename))
  return absolute_paths

def copy_to(paths, dir):
  try:
    os.mkdir(dir)
  except OSError:
    print('Directory already exists.')
  for path in paths:
    shutil.copy(path, dir)
  return

def zip_to(paths, zip_file):
  arguments = ['zip', '-j', zip_file]
  arguments.extend(paths)
  print('Calling: ' + ' '.join(arguments))
  subprocess.call(arguments)
  return

def main():
  # This basic command line argument parsing code is provided.
  # Add code to call your functions below.

  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]
  if not args:
    print("usage: [--todir dir][--tozip zipfile] dir [dir ...]")
    sys.exit(1)

  # todir and tozip are either set from command line
  # or left as the empty string.
  # The args array is left just containing the dirs.
  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  tozip = ''
  if args[0] == '--tozip':
    tozip = args[1]
    del args[0:2]

  if len(args) == 0:
    print("error: must specify one or more dirs")
    sys.exit(1)

  if todir:
    copy_to(get_special_paths(args[0]), todir)
  elif tozip:
    zip_to(get_special_paths(args[0]), tozip)
  else:
    print('\n'.join(get_special_paths(args[0])) + '\n')

  
if __name__ == "__main__":
  main()
