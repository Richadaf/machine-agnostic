#!usr/bin/env python
#   user-config.py  Copyright (C) 2021 Richard Famoroti
# -*- coding: utf-8 -*-
# Moves all hidden folders|file in 'fromDir' to 'toDir' and put a symbolic link for them back to 'fromDir'

import argparse
import pathlib
import os
import shutil

def isDir(path):
    return True if os.path.isdir(path) else False
def isLink(path):
	return True if os.path.islink(path) else False

def ignoreFile(filename):
	ignoreFiles = ['.Trash']
	return (len(list(filter (lambda name : name == filename, ignoreFiles))) > 0)
# Parse Argument Input if available
parser = argparse.ArgumentParser(
    description='Symbolic link all hidden files and folders to dir')
parser.add_argument('-f','--fromDir', type=pathlib.Path, nargs=1, help='<Required> Directory to move files from...Usually your home folder', metavar='path/to/dir', required=True)
parser.add_argument('-t', '--toDir', type=pathlib.Path, nargs=1, help='<Required> Directory to move files to...Usually a cloud folder', metavar='path/to/dir', required=True)
parser.add_argument('--version', action='version', version='%(prog)s 1.0')

args = parser.parse_args()

fromDir = str(args.fromDir[0])
toDir = str(args.toDir[0])

try:
	for filename in os.listdir(fromDir):
		fullPath_From = os.path.join(fromDir, filename);
		fullPath_To = os.path.join(toDir, filename);
		if filename.startswith('.') and isDir(fullPath_From) and isLink(fullPath_From) == False and ignoreFile(filename) == False:
			shutil.move(fullPath_From, fullPath_To)
			os.symlink(fullPath_To, fullPath_From, target_is_directory = True, dir_fd = None)
		elif filename.startswith('.') and isDir(fullPath_From) == False and isLink(fullPath_From) == False and ignoreFile(filename) == False:
			shutil.move(fullPath_From, fullPath_To)
			os.symlink(fullPath_To, fullPath_From, target_is_directory = False, dir_fd = None)
except Exception as e:
	print('[Error]:' + e)