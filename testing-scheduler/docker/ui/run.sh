conductor_network='conductor_default'
group="x-lab"
# ui image name
ui_image="$group/testing-scheduler:ui"
# ui container name
ui_container="t-scheduler-ui"

docker run -d --rm -p 5311:5311 --net=$conductor_network --name $ui_container $ui_image
