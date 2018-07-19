# get the absolute path of this shell file.
basepath=$(cd `dirname $0`; pwd)

# get the root directory of this project
projectpath=$basepath/../..
group="x-lab"

# server image name
server_image="$group/testing-scheduler:server"

docker build -t $server_image -f $basepath/Dockerfile  $projectpath