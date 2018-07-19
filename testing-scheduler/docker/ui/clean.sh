group="x-lab"
# ui image name
ui_image="$group/testing-scheduler:ui"
# ui container name
ui_container="t-scheduler-ui"
docker rm -f $ui_container
docker rmi $ui_image
# get the absolute path of this shell file.
basepath=$(cd `dirname $0`; pwd)
rm -rf $basepath/dist