# get the absolute path of this shell file.
basepath=$(cd `dirname $0`; pwd)
tmppath=$basepath/tmp_files
cd $tmppath/conductor/docker
docker-compose -p conductor up -d