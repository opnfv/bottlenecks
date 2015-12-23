#!/bin/bash

function usage()
{
    echo -e "install:
    install [path];
    -->ops:
        path: path of the souce code, default : './'
    "
}

function install()
{
    local file=$1
    local dir=${file%.tar.gz}
    tar -zxvf $file
    cd $dir
    if [ -e "configure" ]; then
        ./configure
    fi
    if [ -e "Makefile" ]; then
        make && make install
        echo "install $dir successfully"
    else
        echo "install $dir failed"
    fi

    cd .. && rm $dir -r

}

if [ $# -gt  2 ]; then
    usage
    exit -1
fi

code_path="./"
if [ $# -eq  2 ]; then
    code_path=$1
fi
cd $code_path
for file in $(ls *.tar.gz);do
    install $file
done

