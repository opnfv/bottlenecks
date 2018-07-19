basepath=$(cd `dirname $0`; pwd)					# get the absolute path of this shell file.
projectpath=$basepath/../..							# get the root directory of this project
group="x-lab"
server_image="$group/testing-scheduler:server"		# server image name
docker build -t $server_image -f $basepath/Dockerfile  $projectpath