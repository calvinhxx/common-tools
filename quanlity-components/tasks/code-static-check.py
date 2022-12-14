#!/usr/bin/python3

import os
import sys
import subprocess

CPPLINTARG = "--filter=-legal/copyright,\
                        -whitespace/line_length,\
                        -build/include_what_you_use,\
                        -build/include,\
                        -whitespace/blank_line,-whitespace/ending_newline,\
                        -build/header_guard,-readability/streams,\
                        -whitespace/parens,-whitespace/operators,\
                        -build/storage_class,\
                        -whitespace/labels,\
                        -build/c++11"

def runcmd(command) -> int: 
    ret = subprocess.run(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8")
    if ret.returncode == 0:
        if ret.stdout != "":
            return 0
        else:
            return 1
    else:
        print(ret.stdout,ret.stderr)
        return -1

def determine_suffix(file):
    suffix = os.path.splitext(file)[-1]
    # print(suffix, type(suffix))
    if  suffix== (".c") or suffix == (".h") or suffix == (".c++") or suffix == (".h++") or suffix == (".cc") or suffix == (".cpp"):
        return True
    else:
        return False

def getcachesfilelist() -> list:
    sh = True
    if sys.platform == 'darwin':
        sh = True
    elif sys.platform == 'win32':
        sh = False
    ret = subprocess.run("git diff --name-only --cached",shell=sh,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8")
    return ret.stdout.split("\n")

if __name__ == '__main__':
    has_error = False
    list = getcachesfilelist()
    for file in list:
        if determine_suffix(file):
            has_error = runcmd("cpplint %s %s"%(CPPLINTARG.replace(" ",""),file))
        else:
            pass
    else:
        if has_error:
            sys.exit(1)
    sys.exit(0)