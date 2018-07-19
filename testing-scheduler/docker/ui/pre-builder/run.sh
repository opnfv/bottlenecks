group="x-lab"
ui_image="$group/testing-scheduler:ui-builder"                          # ui image name
ui_container='t-scheduler-ui-builder'                                   # ui container name
basepath=$(cd `dirname $0`; pwd)                                        # get the absolute path of this shell file.
docker run -d --name $ui_container $ui_image

docker cp $ui_container:/home/testing-scheduler/ui/dist $basepath/../
docker rm -f $ui_container
docker rmi $ui_image