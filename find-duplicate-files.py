#!/usr/bin/env python

import os, hashlib, stat, sys, getopt
from os.path import join, getsize, islink


# returns a list of files with full path
def get_files_list(path):
    files_list = []
    walklist = os.walk(path)
    
    for path, dirs, files in walklist:
        for file in files:
            files_list.append(join(path, file))
    return files_list


# returns md5 hash of a file
def get_md5(file):
    BLOCKSIZE = 65536
    hasher = hashlib.md5()
    with open(file, 'rb') as f:
        buffer = f.read(BLOCKSIZE)
        while len(buffer) > 0:
            hasher.update(buffer)
            buffer = f.read(BLOCKSIZE)
    return hasher.hexdigest()


# returns a list of hashed files with sizes in bytes
def get_hashed_files_list(files_list):
    hashed_files_list = []
    for file in files_list:
        if not islink(file) and not is_socket(file):
            size = getsize(file)
            md5hash = get_md5(file)
            entry = [size, md5hash, file]
            hashed_files_list.append(entry)
    return hashed_files_list


# returns if file is a socket
def is_socket(file):
    mode = os.stat(file).st_mode
    isSocket = stat.S_ISSOCK(mode)
    return isSocket


# return a list of duplicate hashes
def get_duplicate_hashes(hashed_files_list):
    seen = set()
    duplicates = []

    for entry in hashed_files_list:
        hash = entry[1]
        if hash not in seen:
            seen.add(hash)
        else:
            if hash not in duplicates:
                duplicates.append(hash)
    return duplicates


# returns a list of duplicate hashed files
def get_duplicate_hashed_files_list(duplicate_hashes_list, hashed_files_list):
    duplicate_hashed_files_list = []
    for hash in duplicate_hashes_list:
        for hashed_file in hashed_files_list:
            if hash in hashed_file:
                duplicate_hashed_files_list.append(hashed_file)
    return duplicate_hashed_files_list


# return a list of duplicate files order by size
def sort_hashed_files(duplicate_hashed_files_list):
    sorted_list = duplicate_hashed_files_list.sort(reverse=True)
    return sorted_list


# return a list of identical directories
def get_identical_dirs(duplicate_hashed_files_list):
    pass


# output the results
def output(sorted_list, output_file):
    # write results to a file
    if output_file:
        with open(output_file, 'w') as f:
            for i in sorted_list:
                f.write('%s %s %s\n' % (i[0], i[1], i[2]) )
    # print output to sdtout
    else:
        for i in sorted_list:
            print i[0], i[1], i[2]


def main(argv):

    path = ''
    output_file = ''

    # process the arguments
    try:
        opts, args = getopt.getopt(argv, 'p:o:', ['path=', 'output='])
    except getopt.GetoptError:
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-p', '--path'):
            path = arg
        if opt in ('-o', '--output'):
            output_file = arg

    if path == '':
        print "Please specify --path"
        sys.exit(2)

    # make the calls, can later be the controller function
    files_list = get_files_list(path)
    hashed_files_list = get_hashed_files_list(files_list)
    duplicate_hashes_list = get_duplicate_hashes(hashed_files_list)
    duplicate_hashed_files_list = get_duplicate_hashed_files_list(duplicate_hashes_list, hashed_files_list)
    #duplicate_hashed_files_list = sort_hashed_files(duplicate_hashed_files_list)
    sorted_list = sorted(duplicate_hashed_files_list, key=lambda entry: entry[0], reverse=True)
    output(sorted_list, output_file)


if __name__ == '__main__':
    main(sys.argv[1:])
