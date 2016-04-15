##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd. and others
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


import subprocess as subp
import sys
from rubbos_collector import RubbosCollector
from uploader import Uploader

def printUsage():
    print "Usage: python process_data.py required_params(**) optional_params([])"
    print "       ** -i|--input   input_data_dir"
    print "       ** -s|--suite   suite_name"
    print "       ** -c|--conf    conf_file"
    print "       [] -o|--output  output_file"
    print "       [] -u|--upload  yes|no"

def process(input_dir, suite_name):
    result = dict()
    if suite_name == "rubbos":
        result = RubbosCollector().collect_data(input_dir)
    return result

def writeResult(output_file, result):
    f = open(output_file, "w")
    if isinstance(result, list):
        for elem in result:
            f.write(str(elem) + "\n")
    f.close()

def uploadResult(conf, suite_name, result):
    Uploader(conf).upload_result(suite_name, result)
    print "upload"

def main():
    if len(sys.argv) < 7 or len(sys.argv) % 2 == 0:
        printUsage()
        exit (1)
    i = 1
    params = dict()
    while (i < len(sys.argv)):
        print sys.argv[i]
        if sys.argv[i]=="-i" or sys.argv[i]=="--input":
            params["input"] = sys.argv[i+1]
        if sys.argv[i]=="-s" or sys.argv[i]=="--suite":
            params["suite"] = sys.argv[i+1]
        if sys.argv[i]=="-c" or sys.argv[i]=="--conf":
            params["conf"] = sys.argv[i+1]
        if sys.argv[i]=="-o" or sys.argv[i]=="--output":
            params["output"] = sys.argv[i+1]
        if sys.argv[i]=="-u" or sys.argv[i]=="--upload":
            params["upload"] = sys.argv[i+1]
        i = i+2
    print params
    if not(params.has_key("input") and params.has_key("suite") and params.has_key("conf")):
        print "Lack some required parameters."
        exit (1)

    result = process(params["input"], params["suite"])
    print "Results:"
    for elem in result:
        print elem

    if params.has_key("output"):
        writeResult(params["output"],result)

    if params.has_key("upload") and params["upload"].lower()=="yes":
        uploadResult(params["conf"], params["suite"], result)

if __name__=="__main__":
    main()
