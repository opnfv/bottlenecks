basepath=$(cd `dirname $0`; pwd)                                        # get the absolute path of this shell file.
projectpath=$basepath/../../..                                                     # get the root directory of this project
ui_image='leoc/testing-scheduler:ui-builder'                            # ui image name
sudo docker build -t $ui_image -f $basepath/Dockerfile $projectpath