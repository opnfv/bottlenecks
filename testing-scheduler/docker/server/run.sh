conductor_network='conductor_default'
group="x-lab"
server_image="$group/testing-scheduler:server"		# server image name
server_container="t-scheduler-server"				# server container name

docker run -d --rm -p 5310:5310 -p 5312:5312 --net=$conductor_network --name $server_container $server_image