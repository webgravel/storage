#!/usr/bin/env python2.7
import sys
import argparse

sys.path.append('/gravel/pkg/gravel-common')
sys.path.append('/gravel/pkg/gravel-node')

import cmd_util
import storage_node

def action_activate():
    parser = argparse.ArgumentParser()
    parser.add_argument('resname')
    args = parser.parse_args()

    storage_node.get_box(args.resname).asked_to_activate()

if __name__ == '__main__':
    cmd_util.chdir_to_code()
    cmd_util.main_multiple_action(globals())
