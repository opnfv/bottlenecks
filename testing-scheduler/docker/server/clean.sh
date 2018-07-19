group="x-lab"
server_image="$group/testing-scheduler:server"		# server image name
server_container="t-scheduler-server"				# server container name

docker rm -f $server_container
docker rmi $server_image