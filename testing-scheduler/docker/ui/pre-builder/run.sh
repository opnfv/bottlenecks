conductor_network='docker_default'
ui_image='leoc/testing-scheduler:ui-builder'                            # ui image name
ui_container='t-scheduler-ui-builder'                                           # ui container name
basepath=$(cd `dirname $0`; pwd)                                        # get the absolute path of this shell file.
sudo docker run -d --name $ui_container $ui_image

sudo docker cp $ui_container:/home/testing-scheduler/ui/dist $basepath/../
sudo docker rm -f $ui_container
sudo docker rmi $ui_image