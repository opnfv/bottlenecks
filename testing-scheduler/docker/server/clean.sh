group="x-lab"
# server image name
server_image="$group/testing-scheduler:server"
# server container name
server_container="t-scheduler-server"

docker rm -f $server_container
docker rmi $server_image