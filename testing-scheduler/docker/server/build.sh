basepath=$(cd `dirname $0`; pwd)					# get the absolute path of this shell file.
projectpath=$basepath/../..							# get the root directory of this project
server_image='leoc/testing-scheduler:server'		# server image name
sudo docker build -t $server_image -f $basepath/Dockerfile  $projectpath