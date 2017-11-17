#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import subprocess
import argparse
from os import path
import os
import re

__author__ = 'yaming'

'''
a tools for check out code for git
'''


parse = argparse.ArgumentParser(description='a tools for check out code for git')

parse.add_argument('--git', '-g', dest='git', help= 'git ssh address', required=True)
parse.add_argument('--tag', '-t', dest='tag', help= 'git tag')
parse.add_argument('--dir', '-d', dest='dir', help= 'local dir', required= True)
parse.add_argument('--verbose', '-v',  dest='verbose', action='store_true', help='Print verbose logging.')

args = parse.parse_args()

git = args.git
tag = args.tag
dir = args.dir
verbose = args.verbose
result = re.match(r'^git@.*:.*/.*.git', git)

local_path = path.abspath(dir)

if verbose:
    print 'git: %s' % git
    print 'tag: %s' % tag
    print 'dir: %s' % local_path

if not git:
    raise ValueError('git address is null')

if not dir:
    raise ValueError('local dir is null')

if not result:
    raise ValueError('not valid git address: %s' % git)


if not path.exists(local_path):
    os.makedirs(local_path)

if not tag:
    tag = 'master'

real_local_path = path.join(local_path, tag)
if not path.exists(local_path):
    os.makedirs(local_path)

command_checkout = 'cd %s && git clone %s %s' % (local_path, git, tag)
command_checkout_tag = 'cd %s && git clone --branch %s %s %s' % (local_path, tag, git, tag)
command_update = 'cd %s && git pull' % real_local_path
command_clean = 'cd %s && git add . && git stash && git stash drop' % real_local_path
command_status = 'cd %s && git status' % real_local_path

is_empty = True
is_clean = True

if path.exists(real_local_path):
    is_empty = len(os.listdir(real_local_path)) <= 0
    if is_empty:
        os.rmdir(real_local_path)
    else:
        status = subprocess.check_output(command_status, shell=True)
        is_clean = 'directory clean' in status

        if not is_clean:
            is_clean = 'tree clean' in status

is_master = 'master' == tag


def clean():
    subprocess.check_call(command_clean, shell=True)


def update():
    subprocess.check_call(command_update, shell=True)


def checkout():
    subprocess.check_call(command_checkout, shell=True)


def checkout_tag():
    subprocess.check_call(command_checkout_tag, shell=True)

if is_empty:
    if is_master:
        checkout()
    else:
        checkout_tag()
    print 'checkout success'
else:
    if is_master:
        if not is_clean:
            clean()
        print ' working directory clean'
        update()
        print 'clean and update master'
    else:
        if not is_clean:
            clean()
            print 'clean %s' % tag
        print ' working directory clean'
        try:
            update()
        except Exception, e:
            print e
            pass


print 'git path: %s' % real_local_path
